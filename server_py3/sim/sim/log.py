#!/usr/bin/env python3

import sys
import logging
from logging.handlers import TimedRotatingFileHandler


default_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)-5s]"
        " [%(process)s:%(processName)s]"
        " [%(threadName)s]"
        " [%(name)s]"
        " [%(filename)s:%(funcName)s:%(lineno)d]"
        " -- %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )


class LoggerManager(object):
    def __init__(self, logger, level=None, fmt=None):
        if isinstance(logger, logging.Logger):
            self.loggers = [logger]
        elif isinstance(logger, (list, tuple)):
            self.loggers = logger
        else:
            raise Exception(f"param logger must be logger/list/tuple, but get a {type(logger)}")

        self.level = level or logging.DEBUG
        self.fmt = fmt or default_formatter

        for lgr in self.loggers:
            lgr.setLevel(self.level)

    def addConsoleHandler(self, level=None, fmt=None):
        """输出到控制台（终端）"""
        for lgr in self.loggers:
            assert isinstance(lgr, logging.Logger)

            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(fmt or self.fmt)
            if level:
                ch.setLevel(level)

            lgr.addHandler(ch)

    def addFileHandler(self, filename, level=None, fmt=None, **kwargs):
        """输出到文件"""
        for lgr in self.loggers:
            assert isinstance(lgr, logging.Logger)

            fh = logging.FileHandler(filename=filename, **kwargs)
            fh.setFormatter(fmt or self.fmt)
            if level:
                fh.setLevel(level)

            lgr.addHandler(fh)

    def addTimedFileHandler(self, filename, level=None, fmt=None, when='MIDNIGHT', **kwargs):
        """输出到文件，可以按时间备份"""
        for lgr in self.loggers:
            assert isinstance(lgr, logging.Logger)

            fh = TimedRotatingFileHandler(filename=filename, when=when, **kwargs)
            fh.setFormatter(fmt or self.fmt)
            if level:
                fh.setLevel(level)

            lgr.addHandler(fh)


def setup_logger(logger, level=logging.DEBUG, log_file=None, fmt=None):
    # logger配置
    formatter = fmt or default_formatter

    # 指定日志的最低输出级别
    logger.setLevel(level)

    # 控制台日志
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # 写日志到文件中
    if log_file:
        fn = log_file
        fh = TimedRotatingFileHandler(filename=fn, when='MIDNIGHT')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

