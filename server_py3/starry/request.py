#!/usr/bin/env python3

import ujson


class Request(object):
    def __init__(self, environ):
        self.env = environ
        self.environ = environ

        self.method = environ.get('REQUEST_METHOD')
        self.path = environ.get('PATH_INFO')
        self.query_string = environ.get('QUERY_STRING')
        self.query = self.parse_query()

        self.content_type = environ.get('CONTENT_TYPE')
        self.content_length = environ.get('CONTENT_LENGTH')
        self.data = None
        self._json = None

        self.params = {}

    def json(self):
        """获取 http body 中的数据，以JSON格式返回"""
        if self._json:
            return self._json

        if self.content_length:
            self.content_length = int(self.content_length)
            stream = self.environ.get('wsgi.input')

            self.data = stream.read(self.content_length)
            if self.content_type == 'application/json':
                self._json = ujson.decode(self.data)

        return self._json

    def parse_query(self):
        if self.query_string:
            pass

    def set_params(self, params):
        self.params = params

    def get_param(self, param):
        return self.params[param]

    def query(self):
        pass

