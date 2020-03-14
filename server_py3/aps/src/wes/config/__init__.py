#!/usr/bin/env python3

import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from sim.application import Application
from sim.log import setup_logger, LoggerManager

env = os.getenv('YONDER_CONFIG') or 'dev'

if env == 'live':
    from .config_live import configs
else:
    from .config_dev import configs


class BaseConfig(object):
    log_level = logging.DEBUG
    configs = configs

    @classmethod
    def init_app(cls, app: Application):
        app.update_config(cls.configs)

        lgm = LoggerManager(
            [app.logger, logging.getLogger('sim')],
            cls.log_level,
        )
        lgm.addConsoleHandler()
        lgm.addTimedFileHandler(filename=cls.configs['LOG_FILE'], backupCount=30)

        # for lgr in [app.logger, logging.getLogger('sim')]:
        #     setup_logger(lgr, level=cls.log_level, log_file=cls.configs['LOG_FILE'])


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
