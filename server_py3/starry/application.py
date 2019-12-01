#!/usr/bin/env python3

"""
todo:

db
middleware
logger
debug loader: auto reload source code in debug mode

done:
json data from http body
parse query string, unquote to utf-8
cookie
"""

import threading

from .httpserver import run_simple
from .tree import Tree
from .exceptions import (AppBaseException, MethodNotAllowed, NotFound, InternalServerError)
from .context import AppRequestContext
from .response import Response
from .log import logger

# context = ctx = threading.local()


class Application(object):
    def __init__(self):
        self._methodTrees = {}
        self._allowMethods = set()

        # handler funcs before request
        # def func(ctx):
        #     pass
        # use `before_request` to add a function
        self.before_request_funcs = []

        # handler funcs after request
        # def handler(ctx, response):
        #     pass
        # use `after_request` to add a handler
        self.after_request_funcs = []

    def run(self, host='localhost', port=8000, **options):
        options.setdefault('threaded', True)
        return run_simple(host, port, self, **options)

    def route(self, rule, **options):
        """添加路由"""
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

    def before_request(self, f):
        self.before_request_funcs.append(f)
        return f

    def after_request(self, f):
        self.after_request_funcs.append(f)
        return f

    def dispatch_request(self, ctx):
        """根据url分发请求到 handler，获取响应"""
        if not self._allowMethods:
            self._allowMethods = set(self._methodTrees.keys())

        method = ctx.request.method.upper()
        if not method:
            raise MethodNotAllowed

        if method not in self._allowMethods:
            raise MethodNotAllowed

        tree = self._methodTrees.get(method)
        if not tree:
            raise NotFound

        # path = ctx.env.get('PATH_INFO')
        path = ctx.request.path
        node, params = tree.search(path)

        # 路径中的参数
        ctx.request.set_params(params)

        if not (node and node.handler):
            raise NotFound

        handler = node.handler
        if not handler.__code__.co_argcount:    # 参数个数
            resp = node.handler()
        else:
            resp = node.handler(ctx)

        return resp

    def load_context(self, environ):
        ctx = AppRequestContext(self, environ)
        return ctx

    def preprocess_request(self, ctx):
        for func in self.before_request_funcs:
            rv = func(ctx)
            if rv is not None:
                return rv

    def process_response(self, ctx, response):
        """
        :param ctx:  AppRequestContext
        :param response:    subclass of Response or AppBaseException
        :return:
        """
        if ctx.cookies:
            ctx.save_session(response)

        for handler in self.after_request_funcs:
            response = handler(ctx, response)
            if response is None:
                logger.error(f"middleware {handler.__name__} return a None response")
                raise InternalServerError()

        return response

    def wsgi_app(self, environ, start_response):
        print()
        print('-' * 50)
        ctx = self.load_context(environ)
        try:
            rv = self.preprocess_request(ctx)
            if rv is None:
                rv = self.dispatch_request(ctx)

            response = Response(rv)
            response = self.process_response(ctx, response)

        except AppBaseException as e:
            logger.exception("http error")
            response = e

        except Exception as e:
            logger.exception("internal error")
            response = InternalServerError()

        result = response(environ, start_response)      # response.__call__()
        print('result:', result)
        return result

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


