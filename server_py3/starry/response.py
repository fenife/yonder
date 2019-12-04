#!/usr/bin/env python3

import ujson
from http.cookies import SimpleCookie

from .status import code2name, code2status
from .log import logger


class Response(object):
    charset = "utf-8"
    default_status_code = 200
    default_mimetype = "text/json"

    # todo: why this line cause content-length error ?
    # default_headers = [('Content-Type', 'text/json')]

    def __init__(self, data=None, code=None, msg=None, headers=None):
        self.data = data
        self.status_code = code or self.default_status_code
        self._msg = msg
        self.mimetype = self.default_mimetype
        self.headers = headers or [('Content-Type', 'text/json')]
        self._cookies = SimpleCookie()

    @property
    def msg(self):
        if self._msg:
            return self._msg

        n = code2name(self.status_code)
        return n

    @property
    def name(self):
        """
        http status name
        :return:
        """
        n = code2name(self.status_code)
        return n

    def _get_status(self):
        if 0 < self.status_code < 1000:
            # 大于0的是HTTP状态码
            return code2status(self.status_code)
        else:
            # 小于0的为自定义的状态码
            # HTTP 状态码返回OK，response的data中才是真正的异常原因
            return "200 OK"

    def _get_headers(self):
        return self.headers

    def _get_body(self):
        if isinstance(self.data, bytes):
            # 返回的格式是固定的，bytes需要手动拼接
            c = b'{"code":' + str(self.status_code).encode(self.charset) + b','
            d = b'"data":"' + self.data + b'",'
            m = b'"msg":"' + self.msg.encode(self.charset) + b'"}'
            body = c + d + m
            return body

        body = {
            "code": self.status_code,
            "data": {} if self.data is None else self.data,
            "msg": self.msg,
        }
        # self.data = ujson.dumps(self.data).encode(self.charset)
        body = ujson.dumps(body).encode(self.charset)
        return body

    def __call__(self, environ, start_response):

        body = self._get_body()
        status = self._get_status()
        headers = self._get_headers()
        start_response(status, headers)

        # print('body len:', len(body))
        return [body]
