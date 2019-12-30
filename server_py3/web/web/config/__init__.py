#!/usr/bin/env python3

import logging
from sim.application import Application

from .config_dev import dev_configs
from .config_live import live_configs


class BaseConfig(object):
    configs = dev_configs
    log_level = logging.DEBUG

    @classmethod
    def init_app(cls, app: Application):
        app.update_config(cls.configs)


class DevConfig(BaseConfig):
    """开发环境的配置"""
    configs = dev_configs
    log_level = logging.DEBUG


class LiveConfig(BaseConfig):
    """线上环境的配置"""
    configs = live_configs
    log_level = logging.INFO

    @classmethod
    def init_app(cls, app: Application):
        app.update_config(cls.configs)

        # 写日志到文件中
        from logging.handlers import TimedRotatingFileHandler
        from sim.log import formatter

        fn = live_configs['LOG_FILE']
        fh = TimedRotatingFileHandler(filename=fn, when='MIDNIGHT')
        fh.setFormatter(formatter)
        app.logger.addHandler(fh)

        app.logger.setLevel(cls.log_level)


config = {
    'dev': DevConfig,
    'live': LiveConfig,
}
