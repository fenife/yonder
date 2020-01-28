#!/usr/bin/env python3

import os
import logging
from sim.application import Application

env = os.getenv('YONDER_CONFIG') or 'dev'

if env == 'live':
    from .config_live import configs
else:
    from .config_dev import configs


class BaseConfig(object):
    configs = configs
    log_level = logging.DEBUG

    @classmethod
    def init_app(cls, app: Application):
        app.update_config(cls.configs)

        # 写日志到文件中
        from logging.handlers import TimedRotatingFileHandler
        from sim.log import formatter

        fn = cls.configs['LOG_FILE']
        fh = TimedRotatingFileHandler(filename=fn, when='MIDNIGHT')
        fh.setFormatter(formatter)
        app.logger.addHandler(fh)

        app.logger.setLevel(cls.log_level)


class DevConfig(BaseConfig):
    """开发环境的配置"""
    log_level = logging.DEBUG


class LiveConfig(BaseConfig):
    """线上环境的配置"""
    log_level = logging.INFO


config = {
    'dev': DevConfig,
    'live': LiveConfig,
}
