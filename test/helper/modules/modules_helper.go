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

package moduleshelper

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"testing"
	"time"

	"cloud.google.com/go/storage"
	"github.com/Azure/azure-sdk-for-go/sdk/storage/azblob"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"google.golang.org/api/iterator"
	"google.golang.org/api/option"

	"github.com/weaviate/weaviate/test/helper"
	graphqlhelper "github.com/weaviate/weaviate/test/helper/graphql"
)

func EnsureClassExists(t *testing.T, className string, tenant string) {
	query := fmt.Sprintf("{Aggregate{%s", className)
	if tenant != "" {
		query += fmt.Sprintf("(tenant:%q)", tenant)
	}
	query += " { meta { count}}}}"
	resp := graphqlhelper.AssertGraphQL(t, helper.RootAuth, query)

	class := resp.Get("Aggregate", className).Result.([]interface{})
	require.Len(t, class, 1)
}

func EnsureCompressedVectorsRestored(t *testing.T, className string) {
	query := fmt.Sprintf("{Get{%s(limit:1){_additional{vector}}}}", className)
	resp := graphqlhelper.AssertGraphQL(t, helper.RootAuth, query)

	class := resp.Get("Get", className).Result.([]interface{})
	require.Len(t, class, 1)
	vecResp := class[0].(map[string]interface{})["_additional"].(map[string]interface{})["vector"].([]interface{})

	searchVec := graphqlhelper.Vec2String(graphqlhelper.ParseVec(t, vecResp))

	limit := 10
	query = fmt.Sprintf(
		"{Get{%s(nearVector:{vector:%s} limit:%d){_additional{vector}}}}",
		className, searchVec, limit)
	resp = graphqlhelper.AssertGraphQL(t, helper.RootAuth, query)
	class = resp.Get("Get", className).Result.([]interface{})
	require.Len(t, class, limit)
}

func GetClassCount(t *testing.T, className string, tenant string) int64 {
	query := fmt.Sprintf("{Aggregate{%s", className)
	if tenant != "" {
		query += fmt.Sprintf("(tenant:%q)", tenant)
	}
	query += " { meta { count}}}}"
	resp := graphqlhelper.AssertGraphQL(t, helper.RootAuth, query)

	class := resp.Get("Aggregate", className).Result.([]interface{})
	require.Len(t, class, 1)

	meta := class[0].(map[string]interface{})["meta"].(map[string]interface{})

	countPayload := meta["count"].(json.Number)

	count, err := countPayload.Int64()
	require.Nil(t, err)

	return count
}

func CreateTestFiles(t *testing.T, dirPath string) []string {
	count := 5
	filePaths := make([]string, count)
	var fileName string

	for i := 0; i < count; i += 1 {
		fileName = fmt.Sprintf("file_%d.db", i)
		filePaths[i] = filepath.Join(dirPath, fileName)
		file, err := os.Create(filePaths[i])
		if err != nil {
			t.Fatalf("failed to create test file '%s': %s", fileName, err)
		}
		fmt.Fprintf(file, "This is content of db file named %s", fileName)
		file.Close()
		t.Logf("Created test file: %s\n", filePaths[i])
	}
	return filePaths
}

func CreateGCSBucket(ctx context.Context, t *testing.T, projectID, bucketName string) {
	assert.EventuallyWithT(t, func(collect *assert.CollectT) {
		client, err := storage.NewClient(ctx, option.WithoutAuthentication())
		assert.Nil(t, err)
		assert.Nil(t, client.Bucket(bucketName).Create(ctx, projectID, nil))
	}, 5*time.Second, 500*time.Millisecond)
}

func DeleteGCSBucket(ctx context.Context, t *testing.T, bucketName string) {
	assert.EventuallyWithT(t, func(collect *assert.CollectT) {
		client, err := storage.NewClient(ctx, option.WithoutAuthentication())
		assert.Nil(t, err)

		bucket := client.Bucket(bucketName)
		// we do iterate over objects because GCP doesn't allow deleting non-empty buckets
		it := bucket.Objects(ctx, nil)
		for {
			objAttrs, err := it.Next()
			if errors.Is(err, iterator.Done) {
				break
			}
			assert.Nil(t, err)

			obj := bucket.Object(objAttrs.Name)
			err = obj.Delete(ctx)
			assert.Nil(t, err)
		}
		assert.Nil(t, bucket.Delete(ctx))
	}, 5*time.Second, 500*time.Millisecond)
}

func CreateAzureContainer(ctx context.Context, t *testing.T, endpoint, containerName string) {
	t.Log("Creating azure container", containerName)
	assert.EventuallyWithT(t, func(collect *assert.CollectT) {
		connectionString := "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://%s/devstoreaccount1;"
		client, err := azblob.NewClientFromConnectionString(fmt.Sprintf(connectionString, endpoint), nil)
		assert.Nil(t, err)

		_, err = client.CreateContainer(ctx, containerName, nil)
		assert.Nil(t, err)
	}, 5*time.Second, 500*time.Millisecond)
}

func DeleteAzureContainer(ctx context.Context, t *testing.T, endpoint, containerName string) {
	assert.EventuallyWithT(t, func(collect *assert.CollectT) {
		connectionString := "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://%s/devstoreaccount1;"
		client, err := azblob.NewClientFromConnectionString(fmt.Sprintf(connectionString, endpoint), nil)
		assert.Nil(t, err)

		_, err = client.DeleteContainer(ctx, containerName, nil)
		assert.Nil(t, err)
	}, 5*time.Second, 500*time.Millisecond)
}
