//                           _       _
// __      _____  __ ___   ___  __ _| |_ ___
// \ \ /\ / / _ \/ _` \ \ / / |/ _` | __/ _ \
//  \ V  V /  __/ (_| |\ V /| | (_| | ||  __/
//   \_/\_/ \___|\__,_| \_/ |_|\__,_|\__\___|
//
//  Copyright © 2016 - 2024 Weaviate B.V. All rights reserved.
//
//  CONTACT: hello@weaviate.io
//

package lsmkv

import (
	"bufio"
	"bytes"
	"encoding/binary"
	"io"

	"github.com/pkg/errors"
	"github.com/weaviate/sroar"
	"github.com/weaviate/weaviate/adapters/repos/db/lsmkv/segmentindex"
)

type compactorInverted struct {
	// c1 is always the older segment, so when there is a conflict c2 wins
	// (because of the replace strategy)
	c1 *segmentCursorInvertedReusable
	c2 *segmentCursorInvertedReusable

	// the level matching those of the cursors
	currentLevel        uint16
	secondaryIndexCount uint16
	// Tells if tombstones or keys without corresponding values
	// can be removed from merged segment.
	// (left segment is root (1st) one, keepTombstones is off for bucket)
	cleanupTombstones bool

	w    io.WriteSeeker
	bufw *bufio.Writer

	scratchSpacePath string

	offset int

	tombstonesToWrite *sroar.Bitmap
	tombstonesToClean *sroar.Bitmap

	keysLen uint64
}

func newCompactorInverted(w io.WriteSeeker,
	c1, c2 *segmentCursorInvertedReusable, level, secondaryIndexCount uint16,
	scratchSpacePath string, cleanupTombstones bool,
) *compactorInverted {
	return &compactorInverted{
		c1:                  c1,
		c2:                  c2,
		w:                   w,
		bufw:                bufio.NewWriterSize(w, 256*1024),
		currentLevel:        level,
		cleanupTombstones:   cleanupTombstones,
		secondaryIndexCount: secondaryIndexCount,
		scratchSpacePath:    scratchSpacePath,
		offset:              0,
	}
}

func (c *compactorInverted) do() error {
	var err error

	if err := c.init(); err != nil {
		return errors.Wrap(err, "init")
	}

	c.offset = segmentindex.HeaderSize

	kis, tombstones, err := c.writeKeys()
	if err != nil {
		return errors.Wrap(err, "write keys")
	}
	c.keysLen = uint64(c.offset - segmentindex.HeaderSize - 8)

	tombstoneSize, err := c.writeTombstones(tombstones)
	if err != nil {
		return errors.Wrap(err, "write tombstones")
	}

	if err := c.writeIndices(kis); err != nil {
		return errors.Wrap(err, "write index")
	}

	// flush buffered, so we can safely seek on underlying writer
	if err := c.bufw.Flush(); err != nil {
		return errors.Wrap(err, "flush buffered")
	}

	var dataEnd uint64 = segmentindex.HeaderSize + 8 + 8 + uint64(tombstoneSize)
	if len(kis) > 0 {
		dataEnd = uint64(kis[len(kis)-1].ValueEnd) + 8 + uint64(tombstoneSize)
	}
	if err := c.writeHeader(c.currentLevel, 0, c.secondaryIndexCount,
		dataEnd); err != nil {
		return errors.Wrap(err, "write header")
	}

	if err := c.writeKeysLength(); err != nil {
		return errors.Wrap(err, "write keys length")
	}

	return nil
}

func (c *compactorInverted) init() error {
	// write a dummy header, we don't know the contents of the actual header yet,
	// we will seek to the beginning and overwrite the actual header at the very
	// end

	if _, err := c.bufw.Write(make([]byte, segmentindex.HeaderSize)); err != nil {
		return errors.Wrap(err, "write empty header")
	}

	return nil
}

func (c *compactorInverted) writeTombstones(tombstones *sroar.Bitmap) (int, error) {
	tombstonesBuffer := make([]byte, 0)

	if tombstones != nil && tombstones.GetCardinality() > 0 {
		tombstonesBuffer = tombstones.ToBuffer()
	}

	buf := make([]byte, 8)
	binary.LittleEndian.PutUint64(buf, uint64(len(tombstonesBuffer)))
	if _, err := c.bufw.Write(buf); err != nil {
		return 0, err
	}

	if _, err := c.bufw.Write(tombstonesBuffer); err != nil {
		return 0, err
	}

	return len(tombstonesBuffer), nil
}

func (c *compactorInverted) writeKeys() ([]segmentindex.Key, *sroar.Bitmap, error) {
	// placeholder for the keys length
	buf := make([]byte, 8)
	binary.LittleEndian.PutUint64(buf, 0)
	if _, err := c.bufw.Write(buf); err != nil {
		return nil, nil, err
	}

	c.offset += 8

	key1, value1, _ := c.c1.first()
	key2, value2, _ := c.c2.first()

	var err error

	c.tombstonesToWrite, err = c.c1.segment.GetTombstones()
	if err != nil {
		return nil, nil, errors.Wrap(err, "get tombstones")
	}

	c.tombstonesToClean, err = c.c2.segment.GetTombstones()
	if err != nil {
		return nil, nil, errors.Wrap(err, "get tombstones")
	}

	// the (dummy) header was already written, this is our initial offset

	var kis []segmentindex.Key
	sim := newSortedMapMerger()

	for {
		if key1 == nil && key2 == nil {
			break
		}
		if bytes.Equal(key1, key2) {

			value1Clean, skip := c.cleanupValues(value1)
			if skip {
				key1, value1, _ = c.c1.next()
				continue
			}

			sim.reset([][]MapPair{value1Clean, value2})
			mergedPairs, err := sim.
				doKeepTombstonesReusable()
			if err != nil {
				return nil, nil, err
			}

			if values, skip := c.cleanupValues(mergedPairs); !skip {
				ki, err := c.writeIndividualNode(c.offset, key2, values)
				if err != nil {
					return nil, nil, errors.Wrap(err, "write individual node (equal keys)")
				}

				c.offset = ki.ValueEnd
				kis = append(kis, ki)
			}
			// advance both!
			key1, value1, _ = c.c1.next()
			key2, value2, _ = c.c2.next()
			continue
		}

		if (key1 != nil && bytes.Compare(key1, key2) == -1) || key2 == nil {
			// key 1 is smaller
			if values, skip := c.cleanupValues(value1); !skip {
				ki, err := c.writeIndividualNode(c.offset, key1, values)
				if err != nil {
					return nil, nil, errors.Wrap(err, "write individual node (key1 smaller)")
				}

				c.offset = ki.ValueEnd
				kis = append(kis, ki)
			}
			key1, value1, _ = c.c1.next()
		} else {
			// key 2 is smaller
			ki, err := c.writeIndividualNode(c.offset, key2, value2)
			if err != nil {
				return nil, nil, errors.Wrap(err, "write individual node (key2 smaller)")
			}

			c.offset = ki.ValueEnd
			kis = append(kis, ki)

			key2, value2, _ = c.c2.next()
		}
	}
	tombstones := c.computeTombstones()

	return kis, tombstones, nil
}

func (c *compactorInverted) writeIndividualNode(offset int, key []byte,
	values []MapPair,
) (segmentindex.Key, error) {
	// NOTE: There are no guarantees in the cursor logic that any memory is valid
	// for more than a single iteration. Every time you call next() to advance
	// the cursor, any memory might be reused.
	//
	// This includes the key buffer which was the cause of
	// https://github.com/weaviate/weaviate/issues/3517
	//
	// A previous logic created a new assignment in each iteration, but thatwas
	// not an explicit guarantee. A change in v1.21 (for pread/mmap) added a
	// reusable buffer for the key which surfaced this bug.
	keyCopy := make([]byte, len(key))
	copy(keyCopy, key)

	return segmentInvertedNode{
		values:     values,
		primaryKey: keyCopy,
		offset:     offset,
	}.KeyIndexAndWriteTo(c.bufw)
}

func (c *compactorInverted) writeIndices(keys []segmentindex.Key) error {
	indices := segmentindex.Indexes{
		Keys:                keys,
		SecondaryIndexCount: c.secondaryIndexCount,
		ScratchSpacePath:    c.scratchSpacePath,
	}

	_, err := indices.WriteTo(c.bufw)
	return err
}

// writeHeader assumes that everything has been written to the underlying
// writer and it is now safe to seek to the beginning and override the initial
// header
func (c *compactorInverted) writeHeader(level, version, secondaryIndices uint16,
	startOfIndex uint64,
) error {
	if _, err := c.w.Seek(0, io.SeekStart); err != nil {
		return errors.Wrap(err, "seek to beginning to write header")
	}

	h := &segmentindex.Header{
		Level:            level,
		Version:          version,
		SecondaryIndices: secondaryIndices,
		Strategy:         segmentindex.StrategyInverted,
		IndexStart:       startOfIndex,
	}

	if _, err := h.WriteTo(c.w); err != nil {
		return err
	}

	return nil
}

// writeKeysLength assumes that everything has been written to the underlying
// writer and it is now safe to seek to the beginning and override the initial
// header
func (c *compactorInverted) writeKeysLength() error {
	if _, err := c.w.Seek(16, io.SeekStart); err != nil {
		return errors.Wrap(err, "seek to beginning to write header")
	}

	buf := make([]byte, 8)
	binary.LittleEndian.PutUint64(buf, c.keysLen)

	_, err := c.w.Write(buf)

	return err
}

// Removes values with tombstone set from input slice. Output slice may be smaller than input one.
// Returned skip of true means there are no values left (key can be omitted in segment)
// WARN: method can alter input slice by swapping its elements and reducing length (not capacity)
func (c *compactorInverted) cleanupValues(values []MapPair) (vals []MapPair, skip bool) {
	// Reuse input slice not to allocate new memory
	// Rearrange slice in a way that tombstoned values are moved to the end
	// and reduce slice's length.
	last := 0
	for i := 0; i < len(values); i++ {
		docId := binary.BigEndian.Uint64(values[i].Key)
		if !(c.tombstonesToClean != nil && c.tombstonesToClean.Contains(docId)) {
			values[last], values[i] = values[i], values[last]
			last++
		}
	}

	if last == 0 {
		return nil, true
	}
	return values[:last], false
}

func (c *compactorInverted) computeTombstones() *sroar.Bitmap {
	if c.cleanupTombstones { // no tombstones to write
		return sroar.NewBitmap()
	}
	if c.tombstonesToWrite == nil {
		return c.tombstonesToClean
	}
	if c.tombstonesToClean == nil {
		return c.tombstonesToWrite
	}
	return sroar.Or(c.tombstonesToWrite, c.tombstonesToClean)
}
