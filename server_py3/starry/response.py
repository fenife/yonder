#!/usr/bin/env python3

import json

from .http import HTTP_STATUS_CODES
from .exceptions import HttpBaseException


class Response(object):
    charset = "utf-8"
    default_status_code = 200
    default_mimetype = "text/json"
    default_headers = [('Content-Type', 'text/json')]

    def __init__(self, response=None, code=None, headers=None):
        self.response = response
        self.status_code = code or self.default_status_code
        self.status_desc = HTTP_STATUS_CODES.get(self.status_code)
        self.mimetype = self.default_mimetype
        self.headers = headers or self.default_headers

    def encode_response(self):
        if isinstance(self.response, bytes):
            return

        if isinstance(self.response, str):
            self.response = self.response.encode(self.charset)

        if isinstance(self.response, HttpBaseException):
            self.status_code = self.response.code
            self.status_desc = HTTP_STATUS_CODES.get(self.status_code)
            resp = {
                "code": self.status_code,
                "data": None,
                "msg": self.status_desc,
            }
            self.response = json.dumps(resp).encode(self.charset)
            return

        self.response = json.dumps(self.response).encode(self.charset)

    def get_status(self):
        status = str(self.status_code) + " " + self.status_desc
        return status

    def get_headers(self):
        return self.headers

    def __call__(self, environ, start_response):
        self.encode_response()

        status = self.get_status()
        headers = self.get_headers()
        start_response(status, headers)

        # todo: the format of response ?
        # {"code": 200, "data": {}, "msg": "success"}

        return [self.response]
