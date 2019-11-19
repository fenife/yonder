#!/usr/bin/env python3

import threading

from .httpd import run_simple
from .tree import Tree

context = ctx = threading.local()


class Response(object):
    pass


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
        method = ctx.env.get('REQUEST_METHOD')
        # todo:
        if not method:
            raise

        tree = self._methodTrees.get(method.upper())
        # todo
        if not tree:
            print('method tree not existed')
            return

        path = ctx.env.get('PATH_INFO')
        node, params = tree.search(path)
        ctx.params = params

        if not node:
            print('no handler found')
            return

        resp = node.handler(ctx)
        return resp

    def make_response(self):
        pass

    def _load_context(self, environ):
        ctx.env = environ
        ctx.environ = environ
        # print(ctx.env)

    def wsgi_app(self, environ, start_response):
        self._load_context(environ)
        resp = self.dispatch_request()
        start_response('200 OK', [('Content-Type', 'text/json')])
        return [resp]
        # return [b"hello web"]

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


