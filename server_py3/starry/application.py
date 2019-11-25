#!/usr/bin/env python3

"""
todo:
json => ujson

db
parse query string
post data
cookie
middleware
logger
"""

import threading

from .httpserver import run_simple
from .tree import Tree
from .exceptions import (AppBaseException, MethodNotAllowed, NotFound)
from .response import Response

context = ctx = threading.local()


class Application(object):
    def __init__(self):
        self._methodTrees = {}
        self._allowMethods = set()

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
        if not self._allowMethods:
            self._allowMethods = set(self._methodTrees.keys())

        method = ctx.method.upper()
        if not method:
            raise MethodNotAllowed

        if method not in self._allowMethods:
            raise MethodNotAllowed

        tree = self._methodTrees.get(method)
        if not tree:
            raise NotFound

        path = ctx.env.get('PATH_INFO')
        node, params = tree.search(path)
        ctx.params = params

        if not (node and node.handler):
            raise NotFound

        handler = node.handler
        if not handler.__code__.co_argcount:    # 参数个数
            resp = node.handler()
        else:
            resp = node.handler(ctx)

        return resp

    def _load_context(self, environ):
        ctx.env = environ
        ctx.environ = environ
        ctx.method = environ.get('REQUEST_METHOD')
        ctx.path = environ.get('PATH_INFO')
        ctx.query = environ.get('QUERY_STRING')
        # print(ctx)

    def make_response(self, rv):
        # assert isinstance(rv, (Response, AppBaseException))
        if isinstance(rv, Response):
            return rv
        if isinstance(rv, AppBaseException):
            return rv

        # if isinstance(rv, tuple):
        #     return Response(*rv)

        return Response(rv)

    def wsgi_app(self, environ, start_response):
        try:
            self._load_context(environ)
            rv = self.dispatch_request()
        except AppBaseException as e:
            rv = e

        response = self.make_response(rv)
        result = response(environ, start_response)      # response.__call__()
        print(result)
        return result

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


