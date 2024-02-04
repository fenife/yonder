#!/usr/bin/env python3

"""
一个自实现的web微框架

暂时只支持返回json数据
"""

import threading
from collections import OrderedDict

from logx import logger

from .httpserver import run_simple
from .tree import Tree
from .exceptions import (AppBaseException, MethodNotAllowed, NotFound, InternalServerError)
from .context import AppRequestContext
from .response import Response


class Application(object):
    def __init__(self, name):
        self.name = name

        # debug mode
        self.debug = False

        # route trees
        self.method_trees = {}

        # allow methods
        self.allow_methods = set()

        # handler funcs before request
        # use `before_request` to add a function
        #
        # @app.before_request
        # def handler(ctx):
        #     pass
        self.before_request_funcs = []

        # handler funcs after request
        # use `after_request` to add a handler
        #
        # @app.after_request
        # def handler(ctx, response):
        #     pass
        self.after_request_funcs = []

        # this logger is for higher application
        self.logger = logger

        # configs
        self.config = {}

    def show_routes(self):
        """
        打印路由树
        """
        print("all routes: ")
        i = 0
        for method, tree in self.method_trees.items():
            routes = tree.get_all_routes()
            # dict排序
            sorted_routes = OrderedDict([(k, routes.get(k)) for k in sorted(routes.keys())])
            # 所有key的最大长度，方便格式化
            ml = max([len(k) for k in sorted_routes.keys()])
            for r, h in sorted_routes.items():
                # r: route, string
                # h: handler, function
                print(' [{m:<4}] {r:<{ml}} -> {h}'.format(m=method, r=r, ml=ml, h=h.__name__))
                i += 1

            print()

        print(f"{i} routes showed")
        print('-' * 50)

    def run(self, host='localhost', port=8000, **options):
        """
        启动app
        :param host: 主机ip，默认为localhost
        :param port: 端口，默认为8000
        :param options:
            show_routes: true/false, 是否打印路由树
        :return:
        """
        # 初始化app的部分属性
        self._init_app(**options)

        # 打印路由树
        show_routes = options.get('show_routes', False)
        if show_routes:
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

        >>> @app.route('/api/test', methods=('GET',))
        >>> def test(ctx):
        ...     pass

        `/api/test`将会被添加到此app的路由树中
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

    def dispatch_request(self, ctx: AppRequestContext):
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

        if not (node and node.handler):
            raise NotFound

        # 路径中的参数
        ctx.request.set_params(params)

        handler = node.handler

        # a class, not a instance
        # if isinstance(handler, type):
        #     # 先实例化，实例化时传入ctx参数;
        #     # 再调用该实例的`__call__()`函数，调用时不会传入任何参数
        #     resp = handler(ctx)()

        if callable(handler):
            resp = handler(ctx)
        else:
            raise Exception("handler is not callable")

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
            # msg = f"`{ctx.method} {ctx.uri}`, msg: {e.msg}, body: {ctx.request.json()}"
            # todo: log request body (if too big)?
            msg = f"`{ctx.method} {ctx.uri}`, msg: {e.msg}, body: {ctx.request.json()}"
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
