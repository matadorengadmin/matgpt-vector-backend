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

// Code generated by go-swagger; DO NOT EDIT.

package authz

// This file was generated by the swagger tool.
// Editing this file might prove futile when you re-run the swagger generate command

import (
	"net/http"

	"github.com/go-openapi/runtime"

	"github.com/weaviate/weaviate/entities/models"
)

// RevokeRoleFromUserOKCode is the HTTP code returned for type RevokeRoleFromUserOK
const RevokeRoleFromUserOKCode int = 200

/*
RevokeRoleFromUserOK Role revoked successfully

swagger:response revokeRoleFromUserOK
*/
type RevokeRoleFromUserOK struct {
}

// NewRevokeRoleFromUserOK creates RevokeRoleFromUserOK with default headers values
func NewRevokeRoleFromUserOK() *RevokeRoleFromUserOK {

	return &RevokeRoleFromUserOK{}
}

// WriteResponse to the client
func (o *RevokeRoleFromUserOK) WriteResponse(rw http.ResponseWriter, producer runtime.Producer) {

	rw.Header().Del(runtime.HeaderContentType) //Remove Content-Type on empty responses

	rw.WriteHeader(200)
}

// RevokeRoleFromUserBadRequestCode is the HTTP code returned for type RevokeRoleFromUserBadRequest
const RevokeRoleFromUserBadRequestCode int = 400

/*
RevokeRoleFromUserBadRequest Bad request

swagger:response revokeRoleFromUserBadRequest
*/
type RevokeRoleFromUserBadRequest struct {

	/*
	  In: Body
	*/
	Payload *models.ErrorResponse `json:"body,omitempty"`
}

// NewRevokeRoleFromUserBadRequest creates RevokeRoleFromUserBadRequest with default headers values
func NewRevokeRoleFromUserBadRequest() *RevokeRoleFromUserBadRequest {

	return &RevokeRoleFromUserBadRequest{}
}

// WithPayload adds the payload to the revoke role from user bad request response
func (o *RevokeRoleFromUserBadRequest) WithPayload(payload *models.ErrorResponse) *RevokeRoleFromUserBadRequest {
	o.Payload = payload
	return o
}

// SetPayload sets the payload to the revoke role from user bad request response
func (o *RevokeRoleFromUserBadRequest) SetPayload(payload *models.ErrorResponse) {
	o.Payload = payload
}

// WriteResponse to the client
func (o *RevokeRoleFromUserBadRequest) WriteResponse(rw http.ResponseWriter, producer runtime.Producer) {

	rw.WriteHeader(400)
	if o.Payload != nil {
		payload := o.Payload
		if err := producer.Produce(rw, payload); err != nil {
			panic(err) // let the recovery middleware deal with this
		}
	}
}

// RevokeRoleFromUserUnauthorizedCode is the HTTP code returned for type RevokeRoleFromUserUnauthorized
const RevokeRoleFromUserUnauthorizedCode int = 401

/*
RevokeRoleFromUserUnauthorized Unauthorized or invalid credentials.

swagger:response revokeRoleFromUserUnauthorized
*/
type RevokeRoleFromUserUnauthorized struct {
}

// NewRevokeRoleFromUserUnauthorized creates RevokeRoleFromUserUnauthorized with default headers values
func NewRevokeRoleFromUserUnauthorized() *RevokeRoleFromUserUnauthorized {

	return &RevokeRoleFromUserUnauthorized{}
}

// WriteResponse to the client
func (o *RevokeRoleFromUserUnauthorized) WriteResponse(rw http.ResponseWriter, producer runtime.Producer) {

	rw.Header().Del(runtime.HeaderContentType) //Remove Content-Type on empty responses

	rw.WriteHeader(401)
}

// RevokeRoleFromUserForbiddenCode is the HTTP code returned for type RevokeRoleFromUserForbidden
const RevokeRoleFromUserForbiddenCode int = 403

/*
RevokeRoleFromUserForbidden Forbidden

swagger:response revokeRoleFromUserForbidden
*/
type RevokeRoleFromUserForbidden struct {

	/*
	  In: Body
	*/
	Payload *models.ErrorResponse `json:"body,omitempty"`
}

// NewRevokeRoleFromUserForbidden creates RevokeRoleFromUserForbidden with default headers values
func NewRevokeRoleFromUserForbidden() *RevokeRoleFromUserForbidden {

	return &RevokeRoleFromUserForbidden{}
}

// WithPayload adds the payload to the revoke role from user forbidden response
func (o *RevokeRoleFromUserForbidden) WithPayload(payload *models.ErrorResponse) *RevokeRoleFromUserForbidden {
	o.Payload = payload
	return o
}

// SetPayload sets the payload to the revoke role from user forbidden response
func (o *RevokeRoleFromUserForbidden) SetPayload(payload *models.ErrorResponse) {
	o.Payload = payload
}

// WriteResponse to the client
func (o *RevokeRoleFromUserForbidden) WriteResponse(rw http.ResponseWriter, producer runtime.Producer) {

	rw.WriteHeader(403)
	if o.Payload != nil {
		payload := o.Payload
		if err := producer.Produce(rw, payload); err != nil {
			panic(err) // let the recovery middleware deal with this
		}
	}
}

// RevokeRoleFromUserNotFoundCode is the HTTP code returned for type RevokeRoleFromUserNotFound
const RevokeRoleFromUserNotFoundCode int = 404

/*
RevokeRoleFromUserNotFound role or user is not found.

swagger:response revokeRoleFromUserNotFound
*/
type RevokeRoleFromUserNotFound struct {

	/*
	  In: Body
	*/
	Payload *models.ErrorResponse `json:"body,omitempty"`
}

// NewRevokeRoleFromUserNotFound creates RevokeRoleFromUserNotFound with default headers values
func NewRevokeRoleFromUserNotFound() *RevokeRoleFromUserNotFound {

	return &RevokeRoleFromUserNotFound{}
}

// WithPayload adds the payload to the revoke role from user not found response
func (o *RevokeRoleFromUserNotFound) WithPayload(payload *models.ErrorResponse) *RevokeRoleFromUserNotFound {
	o.Payload = payload
	return o
}

// SetPayload sets the payload to the revoke role from user not found response
func (o *RevokeRoleFromUserNotFound) SetPayload(payload *models.ErrorResponse) {
	o.Payload = payload
}

// WriteResponse to the client
func (o *RevokeRoleFromUserNotFound) WriteResponse(rw http.ResponseWriter, producer runtime.Producer) {

	rw.WriteHeader(404)
	if o.Payload != nil {
		payload := o.Payload
		if err := producer.Produce(rw, payload); err != nil {
			panic(err) // let the recovery middleware deal with this
		}
	}
}

// RevokeRoleFromUserInternalServerErrorCode is the HTTP code returned for type RevokeRoleFromUserInternalServerError
const RevokeRoleFromUserInternalServerErrorCode int = 500

/*
RevokeRoleFromUserInternalServerError An error has occurred while trying to fulfill the request. Most likely the ErrorResponse will contain more information about the error.

swagger:response revokeRoleFromUserInternalServerError
*/
type RevokeRoleFromUserInternalServerError struct {

	/*
	  In: Body
	*/
	Payload *models.ErrorResponse `json:"body,omitempty"`
}

// NewRevokeRoleFromUserInternalServerError creates RevokeRoleFromUserInternalServerError with default headers values
func NewRevokeRoleFromUserInternalServerError() *RevokeRoleFromUserInternalServerError {

	return &RevokeRoleFromUserInternalServerError{}
}

// WithPayload adds the payload to the revoke role from user internal server error response
func (o *RevokeRoleFromUserInternalServerError) WithPayload(payload *models.ErrorResponse) *RevokeRoleFromUserInternalServerError {
	o.Payload = payload
	return o
}

// SetPayload sets the payload to the revoke role from user internal server error response
func (o *RevokeRoleFromUserInternalServerError) SetPayload(payload *models.ErrorResponse) {
	o.Payload = payload
}

// WriteResponse to the client
func (o *RevokeRoleFromUserInternalServerError) WriteResponse(rw http.ResponseWriter, producer runtime.Producer) {

	rw.WriteHeader(500)
	if o.Payload != nil {
		payload := o.Payload
		if err := producer.Produce(rw, payload); err != nil {
			panic(err) // let the recovery middleware deal with this
		}
	}
}
