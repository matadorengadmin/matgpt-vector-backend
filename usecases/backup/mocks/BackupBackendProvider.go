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

// Code generated by mockery v2.43.2. DO NOT EDIT.

package mocks

import (
	mock "github.com/stretchr/testify/mock"
	modulecapabilities "github.com/weaviate/weaviate/entities/modulecapabilities"
)

// BackupBackendProvider is an autogenerated mock type for the BackupBackendProvider type
type BackupBackendProvider struct {
	mock.Mock
}

// BackupBackend provides a mock function with given fields: backend
func (_m *BackupBackendProvider) BackupBackend(backend string) (modulecapabilities.BackupBackend, error) {
	ret := _m.Called(backend)

	if len(ret) == 0 {
		panic("no return value specified for BackupBackend")
	}

	var r0 modulecapabilities.BackupBackend
	var r1 error
	if rf, ok := ret.Get(0).(func(string) (modulecapabilities.BackupBackend, error)); ok {
		return rf(backend)
	}
	if rf, ok := ret.Get(0).(func(string) modulecapabilities.BackupBackend); ok {
		r0 = rf(backend)
	} else {
		if ret.Get(0) != nil {
			r0 = ret.Get(0).(modulecapabilities.BackupBackend)
		}
	}

	if rf, ok := ret.Get(1).(func(string) error); ok {
		r1 = rf(backend)
	} else {
		r1 = ret.Error(1)
	}

	return r0, r1
}

// EnabledBackupBackends provides a mock function with given fields:
func (_m *BackupBackendProvider) EnabledBackupBackends() []modulecapabilities.BackupBackend {
	ret := _m.Called()

	if len(ret) == 0 {
		panic("no return value specified for EnabledBackupBackends")
	}

	var r0 []modulecapabilities.BackupBackend
	if rf, ok := ret.Get(0).(func() []modulecapabilities.BackupBackend); ok {
		r0 = rf()
	} else {
		if ret.Get(0) != nil {
			r0 = ret.Get(0).([]modulecapabilities.BackupBackend)
		}
	}

	return r0
}

// NewBackupBackendProvider creates a new instance of BackupBackendProvider. It also registers a testing interface on the mock and a cleanup function to assert the mocks expectations.
// The first argument is typically a *testing.T value.
func NewBackupBackendProvider(t interface {
	mock.TestingT
	Cleanup(func())
}) *BackupBackendProvider {
	mock := &BackupBackendProvider{}
	mock.Mock.Test(t)

	t.Cleanup(func() { mock.AssertExpectations(t) })

	return mock
}
