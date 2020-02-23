#!/usr/bin/env python3

import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from sim.application import Application

env = os.getenv('YONDER_CONFIG') or 'dev'

if env == 'live':
    from .config_live import configs
else:
    from .config_dev import configs


class BaseConfig(object):
    # logger配置
    fmt = "\n%(asctime)s||lv=%(levelname)s||f=%(filename)s||func=%(funcName)s||line=%(lineno)d:: %(message)s"
    # fmt = "\n%(asctime)s||lv=%(levelname)s||f=%(filename)s||func=%(funcName)s||line=%(lineno)d:: %(message)s"
    # " [%(process)s: %(threadName)s]" \
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)5s] [%(name)s]" 
        " [%(filename)s:%(funcName)s:%(lineno)d]" 
        " -- %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    log_level = logging.DEBUG

    configs = configs

    @classmethod
    def setup_logger(cls, logger):
        # 指定日志的最低输出级别
        logger.setLevel(cls.log_level)

        # 控制台日志
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(cls.formatter)
        logger.addHandler(ch)

        # 写日志到文件中
        fn = cls.configs['LOG_FILE']
        fh = TimedRotatingFileHandler(filename=fn, when='MIDNIGHT')
        fh.setFormatter(cls.formatter)
        logger.addHandler(fh)

    @classmethod
    def init_app(cls, app: Application):
        app.update_config(cls.configs)

        cls.setup_logger(app.logger)

        sim_logger = logging.getLogger('sim')
        sim_logger.handlers = []
        cls.setup_logger(sim_logger)
        # app.logger = sim_logger


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
