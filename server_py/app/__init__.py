#!/usr/bin/env python3

import os
import sys


cur_path = os.path.dirname(os.path.abspath(__file__))
server_path = os.path.abspath(os.path.join(cur_path, ".."))
home_path = os.path.abspath(os.path.join(server_path, ".."))
pylib_path = os.path.join(home_path, "pylib")
print(f"\ncur_path: {cur_path}, server_path: {server_path}, home_path: {home_path}, pylib_path: {pylib_path}")
sys.path.append(pylib_path)

from lime.application import Application
from lime.norm import Database
from lime.cache import AppCachePool

from app.config import AppConfig


APP_NAME = 'app'

db = Database()
cache_pool = AppCachePool()


def create_app():
    """
    :param config_name: dev/live
    :return:
    """
    app = Application(APP_NAME)

    AppConfig.init_app(app)

    db.init_app(app)
    cache_pool.init_app(app)

    return app


app = create_app()

# 让Python加载模块，否则app.route装饰器不会运行，无法添加路由
from . import api
