#!/usr/bin/env python3


from .http import HTTP_STATUS_CODES


class HttpBaseException(Exception):
    code = None
    desc = HTTP_STATUS_CODES.get(code)

    def __call__(self, environ=None):
        pass


class BadRequest(HttpBaseException):
    code = 400


class Unauthorized(HttpBaseException):
    code = 401


class Forbidden(HttpBaseException):
    code = 403


class NotFound(HttpBaseException):
    code = 404


class MethodNotAllowed(HttpBaseException):
    code = 405


class RequestTimeout(HttpBaseException):
    code = 405


class InternalServerError(HttpBaseException):
    code = 500
