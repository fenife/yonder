#!/usr/bin/env python3

import logging
from sim.application import Application

configs = {
    # app debug mode
    "DEBUG_MODE": True,

    # database config
    "DB_HOST": '127.0.0.1',
    "DB_PORT": 3306,
    "DB_USER": "test",
    "DB_PASSWORD": "test",
    "DB_NAME": "test",
    "DB_CHARSET": "utf8",

    # cache/redis config
    "REDIS_HOST": '127.0.0.1',
    "REDIS_PORT": 6379,

    # web app secret key to gen session token
    "SECRET_KEY": "a key hard to guess",

    # web admin user
    "ADMIN_USERNAME": 'admin',
    "ADMIN_PASSWORD": 'admin',

    # page
    "PAGE_SIZE": 10,

    # 用户登录过期时间
    # login expired time (seconds)
    "LOGIN_EXPIRED": 30 * 60,

    # log file path
    "LOG_FILE": "logs/app.log"
}


