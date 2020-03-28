#!/usr/bin/env python3


from .response import Response
from .status import code2name, code2status


class AppBaseException(Exception):
    code = None

    def __init__(self, code=None, msg=None):
        super(AppBaseException, self).__init__()
        if code is not None:
            self.code = code        # 覆盖class的code属性

        self.msg = msg
        if msg is None:
            self.msg = code2name(self.code)

    def get_response(self):
        return Response(code=self.code, msg=self.msg)

    def __call__(self, environ, start_response):
        response = self.get_response()
        resp = response(environ, start_response)
        return resp


def abort(code, msg=None):
    raise AppBaseException(code, msg)


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


