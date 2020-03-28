#!/usr/bin/env python3

import sys
import os
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
    def __init__(self, logger, level=None, fmt=None, exlog=True):
        """
        logger 管理器，方便为多个logger添加相同的配置
        :param logger:  单个logger, logger的list
        :param level:   log level
        :param fmt:     log formatter
        :param exlog:   默认True，把当前库的logger加上；False则默认不加，
                        但仍可以在`logger`参数中指定
        usage:
        >>> log1 = logging.getLogger('log1')
        >>> log2 = logging.getLogger('log2')
        >>> lgm = LoggerManager([log1, log2], level=logging.DEBUG)
        >>> lgm.addConsoleHandler()
        """
        if isinstance(logger, logging.Logger):
            self.loggers = [logger]
        elif isinstance(logger, (list, tuple)):
            self.loggers = logger
        else:
            raise Exception(f"params logger should be logger/list/tuple, but get a {type(logger)}")

        self.loggers = set(self.loggers)
        if exlog:
            # log name 必须是当前库的顶级目录名，python加载模块时也是用的该名称
            self.loggers.add(logging.getLogger(os.path.basename(os.getcwd())))

        self.level = level or logging.DEBUG
        self.fmt = fmt or default_formatter

        for lgr in self.loggers:
            lgr.setLevel(self.level)

    def addConsoleHandler(self, level=None, fmt=None):
        """输出到控制台"""
        for lgr in self.loggers:
            assert isinstance(lgr, logging.Logger)

            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(fmt or self.fmt)
            if level:
                ch.setLevel(level)

            lgr.addHandler(ch)

    def addFileHandler(self, filename, level=None, fmt=None, **kwargs):
        self._mkdirIfNotExists(filename)

        for lgr in self.loggers:
            assert isinstance(lgr, logging.Logger)

            fh = logging.FileHandler(filename=filename, **kwargs)
            fh.setFormatter(fmt or self.fmt)
            if level:
                fh.setLevel(level)

            lgr.addHandler(fh)

    def addTimedFileHandler(self, filename, level=None, fmt=None, when='MIDNIGHT', **kwargs):
        self._mkdirIfNotExists(filename)

        for lgr in self.loggers:
            assert isinstance(lgr, logging.Logger)

            fh = TimedRotatingFileHandler(filename=filename, when=when, **kwargs)
            fh.setFormatter(fmt or self.fmt)
            if level:
                fh.setLevel(level)

            lgr.addHandler(fh)

    @staticmethod
    def _mkdirIfNotExists(filename):
        # 检查log目录是否存在，不存在则创建
        log_path = os.path.dirname(filename)
        if not os.path.exists(log_path):
            print(f"mkdir for log: `{log_path}`")
            os.makedirs(log_path)


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

