#!/usr/bin/env python3


from .response import Response


class AppBaseException(Exception):
    code = None
    desc = None     # 暂时没用到

    def __init__(self, desc=None):
        super(AppBaseException, self).__init__()
        if desc:
            self.desc = desc

    def get_response(self):
        return Response(code=self.code)

    def __call__(self, environ, start_response):
        response = self.get_response()
        resp = response(environ, start_response)
        return resp


#
# HTTP Exceptions
#


class HttpBaseException(AppBaseException):
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


