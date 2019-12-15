#!/usr/bin/env python3

import json
from http.cookies import SimpleCookie
from .log import logger
from .exceptions import abort


class Request(object):
    def __init__(self, environ):
        self.env = environ
        self.environ = environ

        self.method = environ.get('REQUEST_METHOD')
        self.path = environ.get('PATH_INFO')
        self.query_string = environ.get('QUERY_STRING')
        self._query = dict()

        self.content_type = environ.get('CONTENT_TYPE')
        self.content_length = environ.get('CONTENT_LENGTH')
        self.data = None
        self._json = None

        self.params = {}
        self._cookies = self.parse_cookies()

    def json(self):
        """获取 http body 中的数据，以JSON格式返回"""
        if self._json:
            return self._json

        self.content_length = int(self.content_length)
        if self.content_length:
            stream = self.environ.get('wsgi.input')

            self.data = stream.read(self.content_length)
            if self.content_type == 'application/json':
                # self._json = json.decode(self.data)
                try:
                    self._json = json.loads(self.data)
                except Exception as e:
                    msg = "http body parse error"
                    logger.error(f"{msg}, data: {self.data}")
                    abort(-1, msg)

        return self._json

    def set_params(self, params):
        """
        url params

        eg: /user/:id       # app route
            /user/100       # http url

        => {'id': '100'}    # params

        :param params:
        :return:
        """
        self.params = params

    def get_param(self, param):
        return self.params.get(param, None)

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

        v = self._query.get(k)
        return v

    def all_query(self):
        if not self._query:
            self.parse_query()

        return self._query

    def parse_cookies(self):
        """
        code from aiohttp.web_request

        http header:
        ('Cookie': 'a=1;b=2')      # 注：用;分隔不同的值，不支持utf8字符、空格等

        => {'a': '1', 'b': '2'}
        :return:
        """
        raw = self.env.get('HTTP_COOKIE', '')
        parsed = SimpleCookie(raw)
        # self._cookies = MappingProxyType({k: v.value for k, v in parsed.items()})
        cookies = {k: v.value for k, v in parsed.items()}
        logger.debug('cookies: {}'.format(cookies))
        return cookies

    @property
    def cookies(self):
        """
        这里是客户端发给服务器的cookies (client -> server)
        如果要获取服务器响应中的cookies，看`AppRequestContext.cookies`
        """
        if self._cookies is not None:
            return self._cookies

        return self.parse_cookies()

    def get_cookie(self, name):
        return self._cookies.get(name, None)
