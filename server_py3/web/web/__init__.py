#!/usr/bin/env python3

import os
import sys

sim_path = os.path.abspath(os.path.join(os.path.dirname(__name__), '..', 'sim'))
print(f"sim_path: {sim_path}")
sys.path.append(sim_path)

# ../../sim dir
from sim.application import Application
from sim.norm import Database
from sim.cache import AppCachePool

# current dir
from . import settings


def create_app(config_name):
    if not config_name:
        config_name = 'default'

    app = Application()
    config = settings.configs[config_name]
    app.update_config(config)

    return app


app = create_app(os.getenv('YONDER_CONFIG') or 'default')
db = Database()
db.init_app(app)

cache_pool = AppCachePool()
cache_pool.init_app(app)

# 让Python加载模块，否则app.route装饰器不会运行，无法添加路由
from . import apis
