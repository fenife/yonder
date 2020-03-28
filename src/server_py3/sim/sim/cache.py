#!/usr/bin/env python3

from redis import Redis


class _ConnContextManager(object):
    def __init__(self, pool):
        self.pool = pool

    def __enter__(self) -> Redis:
        r = Redis(self.pool.host, self.pool.port)
        return r

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class AppCachePool(object):
    """
    redis连接池，以做缓存
    暂时未实现连接池功能，每次返回新的连接
    """
    def __init__(self, app=None):
        self.app = app
        self.host = None
        self.port = None

        if self.app is not None:
            self.init_app(self.app)

    def init_app(self, app):
        from .application import Application
        assert isinstance(app, Application)

        if self.app is None:
            self.app = app

        self.host = self.app.config["REDIS_HOST"]
        self.port = self.app.config["REDIS_PORT"]

    def get(self) -> _ConnContextManager:
        c = _ConnContextManager(self)
        return c
