#!/usr/bin/env python3

import json
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
            # HTTP状态码一般是3位的十进制数字
            return code2status(self.status_code)
        else:
            # 其他的为自定义的状态码
            # HTTP 状态码返回OK，response的code才是真正的异常原因
            return "200 OK"

    def _get_headers(self):
        return self.headers

    @property
    def resp_code(self):
        """
        返回response自定义的状态码，不同于http状态码，用于响应的body中
        0    表示成功
        -1   表示错误
        其他 自定义的状态码
        :return:
        """
        # http status code
        if 0 < self.status_code < 1000:
            if self.status_code == 200:
                # success
                return 0
            else:
                # failed
                return -1

        # other custom code
        else:
            return self.status_code

    def _get_body(self):
        if isinstance(self.data, bytes):
            # 返回的格式是固定的，bytes需要手动拼接
            c = b'{"code":' + str(self.resp_code).encode(self.charset) + b','
            d = b'"data":' + self.data + b','
            m = b'"msg":"' + self.msg.encode(self.charset) + b'"}'
            body = c + d + m
            return body

        # object final result:
        # b'{"code":200,"data":{"a":1,"b":2},"msg":"OK"}'

        # bytes resp:
        # b'{"a": 1, "b": 2}'
        # final result:
        # b'{"code":200,"data":"{"a": 1, "b": 2}","msg":"OK"}'

        body = {
            "code": self.resp_code,
            "data": self.data,
            "msg": self.msg,
        }
        body = json.dumps(body, default=str).encode(self.charset)
        return body

    def __call__(self, environ, start_response):

        body = self._get_body()
        status = self._get_status()
        headers = self._get_headers()
        start_response(status, headers)

        # print('body len:', len(body))
        # print('body:', body)
        return [body]
