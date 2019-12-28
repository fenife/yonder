#!/usr/bin/env python3

import logging
from sim.application import Application

_dev_configs = {
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
    "LOG_FILE": "./app.log"
}


# merge dev configs and other configs
_live_configs = {
    **_dev_configs,

    # these configs will overwrite dev configs
    **{
        "DEBUG_MODE": False
    }
}


class BaseConfig(object):
    configs = _dev_configs
    log_level = logging.DEBUG

    @classmethod
    def init_app(cls, app: Application):
        app.update_config(cls.configs)


class DevConfig(BaseConfig):
    """开发环境的配置"""
    configs = _dev_configs
    log_level = logging.DEBUG


class LiveConfig(BaseConfig):
    """线上环境的配置"""
    configs = _live_configs
    log_level = logging.INFO

    @classmethod
    def init_app(cls, app: Application):
        app.update_config(cls.configs)

        # 写日志到文件中
        from logging.handlers import TimedRotatingFileHandler
        from sim.log import formatter

        fn = _live_configs['LOG_FILE']
        fh = TimedRotatingFileHandler(filename=fn, when='d')
        fh.setFormatter(formatter)
        app.logger.addHandler(fh)

        app.logger.setLevel(cls.log_level)


config = {
    'default': DevConfig,
    'dev': DevConfig,
    'live': LiveConfig,
}
