#!/usr/bin/env python3

import os
import sys
import logging

sim_path = os.path.abspath(os.path.join(os.path.dirname(__name__), '..'))
print(f"sim_path: {sim_path}")
sys.path.append(sim_path)

# ../../sim dir
from sim.application import Application
from sim.norm import Database
from sim.log import logger
from sim.cache import AppCachePool


logger.setLevel(logging.DEBUG)


dev_configs = {
    # database config
    "DB_HOST": '127.0.0.1',
    "DB_PORT": 3306,
    "DB_USER": "test",
    "DB_PASSWORD": "test",
    "DB_NAME": "test",
    "DB_CHARSET": "utf8",

    "REDIS_HOST": '127.0.0.1',
    "REDIS_PORT": 6379,
}


app = Application()
app.update_config(dev_configs)
db = Database()
db.init_app(app)

cache_pool = AppCachePool()
cache_pool.init_app(app)
