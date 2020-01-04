#!/usr/bin/env python3

"""
todo:
name: sim, yon

db
del_cookie
add request id
config

done:
json data from http body
parse query string, unquote to utf-8
cookie
middleware
debug loader: auto reload source code in debug mode
logger
"""

import threading
import logging

from .httpserver import run_simple
from .tree import Tree
from .exceptions import (AppBaseException, MethodNotAllowed, NotFound, InternalServerError)
from .context import AppRequestContext
from .response import Response
from .log import logger


class Application(object):
    def __init__(self):
        # debug mode
        self.debug = False

        # route trees
        self.method_trees = {}

        # allow methods
        self.allow_methods = set()

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

        # this logger is for higher application
        self.logger: logging.Logger = logger

        # configs
        self.config = {}

    def show_routes(self):
        # print('-' * 50)
        print("routes: ")
        for method, tree in self.method_trees.items():
            print(f"method: [{method}]")
            tree.print_tree()
            print()

    def run(self, host='localhost', port=8000, **options):
        # 初始化app的部分属性
        self._init_app(**options)

        if self.debug:
            self.show_routes()

        options.setdefault('threaded', True)
        return run_simple(host, port, self, **options)

    def _init_app(self, **options):
        self.debug = self.config.get("DEBUG_MODE", False)

    def update_config(self, configs):
        assert isinstance(configs, dict), f"configs must be a dict"
        self.config.update(configs)

    def route(self, rule, **options):
        """
        装饰器，为app添加路由，装饰的函数将作为该路由的处理函数

        :param rule:    str, url路由规则
        :param options: 其他选项
        目前支持`methods`，为添加的路由指定http请求方法(GET,POST,PUT,...)

        例子：
        >>> app = Application()

        >>> @group.route('/api/test', methods=('GET',))
        >>> def test(ctx):
        ...     pass

        `/api/test`就会被添加到此app的路由树中
        """
        def decorator(f):
            # options.setdefault('methods', ('GET', ))
            methods = options.get('methods', ('GET', ))
            for method in methods:
                method = method.upper()
                tree = self.method_trees.get(method)
                if not tree:
                    tree = Tree()
                    self.method_trees[method] = tree

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
        if not self.allow_methods:
            self.allow_methods = set(self.method_trees.keys())

        method = ctx.request.method.upper()
        if not method or method not in self.allow_methods:
            raise MethodNotAllowed

        tree = self.method_trees.get(method)
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
                self.logger.error(f"middleware {handler.__name__} return a None response")
                raise InternalServerError()

        return response

    def make_response(self, rv):
        if isinstance(rv, Response):
            return rv

        return Response(rv)

    def wsgi_app(self, environ, start_response):
        # print()
        # print('-' * 50)
        ctx = self.load_context(environ)
        try:
            rv = self.preprocess_request(ctx)
            if rv is None:
                rv = self.dispatch_request(ctx)

            response = self.make_response(rv)
            response = self.process_response(ctx, response)

        except AppBaseException as e:
            msg = f"`{ctx.method} {ctx.uri}`, msg: {e.msg}"
            if self.debug:
                self.logger.exception(msg)
            else:
                self.logger.error(msg)

            response = e

        except Exception as e:
            self.logger.exception("internal error")
            response = InternalServerError()

        result = response(environ, start_response)      # response.__call__()
        # print('result:', result)
        return result

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


class RouteGroup(object):
    """
    定义一个路由组，该路由组将以 base_rule 为url的前缀

    1. 可以像下面这样使用：

    >>> app = Application()
    >>> group = RouteGroup(app, base_rule='/api')

    则此路由组会以`/api`作为url的前缀
    然后添加一个路由url规则：

    >>> @group.route('/test')
    >>> def test_group(ctx):
    ...     pass

    则完整的url为：`/api/test`

    2. 不同于`app.route()`函数，`app.route()`中，其参数就是完整的url规则，
    不添加任何前缀，比如：
    >>> @app.route('/test')
    >>> def test_app(ctx):
    ...     pass

    则其完整的url为`/test`
    """
    def __init__(self, app: Application, base_rule: str):
        self.app = app
        self.base_rule = base_rule

    def route(self, rule: str, **options):
        """在路由组中添加一个路由"""
        def decorator(f):
            full_rule = self.base_rule + rule

            methods = options.get('methods', ('GET', ))
            for method in methods:
                method = method.upper()
                tree = self.app.method_trees.get(method)
                if not tree:
                    tree = Tree()
                    self.app.method_trees[method] = tree

                tree.insert(full_rule, f)

            return f

        return decorator
