#!/usr/bin/env python3

"""
todo:
json => ujson
db
"""

import threading
import json

from .httpserver import run_simple
from .tree import Tree
from .exceptions import (HTTP_STATUS_CODES, HttpBaseException, MethodNotAllowed, NotFound)

context = ctx = threading.local()


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


class Application(object):
    def __init__(self):
        self._methodTrees = {}

    def run(self, host='localhost', port=8000, **options):
        options.setdefault('threaded', True)
        return run_simple(host, port, self, **options)

    def route(self, rule, **options):

        def decorator(f):
            # options.setdefault('methods', ('GET', ))
            methods = options.get('methods', ('GET', ))
            for method in methods:
                tree = self._methodTrees.get(method)
                if not tree:
                    tree = Tree()
                    self._methodTrees[method.upper()] = tree

                tree.insert(rule, f)

            return f

        return decorator

    def dispatch_request(self):
        if not ctx.method:
            raise MethodNotAllowed

        tree = self._methodTrees.get(ctx.method.upper())
        if not tree:
            raise NotFound

        path = ctx.env.get('PATH_INFO')
        node, params = tree.search(path)
        ctx.params = params

        if not (node and node.handler):
            raise NotFound

        resp = node.handler(ctx)
        return resp

    def _load_context(self, environ):
        ctx.env = environ
        ctx.environ = environ
        ctx.method = environ.get('REQUEST_METHOD')
        ctx.path = environ.get('PATH_INFO')
        # print(ctx)

    def make_response(self, rv):
        if isinstance(rv, Response):
            return rv
        if isinstance(rv, HttpBaseException):
            return Response(rv)
        if isinstance(rv, tuple):
            return Response(*rv)

        return Response(rv)

    def wsgi_app(self, environ, start_response):
        try:
            self._load_context(environ)
            rv = self.dispatch_request()
        except HttpBaseException as e:
            rv = e

        response = self.make_response(rv)
        result = response(environ, start_response)      # response.__call__()
        # print(result)
        return result

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


