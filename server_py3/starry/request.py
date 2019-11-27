#!/usr/bin/env python3

import ujson


class Request(object):
    def __init__(self, environ):
        self.env = environ
        self.environ = environ

        self.method = environ.get('REQUEST_METHOD')
        self.path = environ.get('PATH_INFO')
        self.query_string = environ.get('QUERY_STRING')
        self._query = None

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

    def set_params(self, params):
        self.params = params

    def get_param(self, param):
        return self.params[param]

    def parse_query(self):
        # a=1&b=2
        print('query_string:', self.query_string)
        if not self.query_string:
            return

        queries = dict()
        for q in self.query_string.split('&'):      # ['a=1', 'b=2']
            item = q.split('=')
            if len(item) == 2:
                k, v = item
                queries[k] = v

        self._query = queries

    def query(self, k):
        if not self._query:
            self.parse_query()

        return self._query[k]

    def all_query(self):
        if not self._query:
            self.parse_query()

        return self._query

