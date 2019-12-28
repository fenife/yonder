#!/usr/bin/env python3

import sys
import logging

# 指定logger输出格式
fmt = "\n%(asctime)s||lv=%(levelname)s||f=%(filename)s||func=%(funcName)s||line=%(lineno)d:: %(message)s"
formatter = logging.Formatter(fmt, datefmt='%Y-%m-%d %H:%M:%S')


def init_stdout_logger(name, level=logging.DEBUG):
    # 获取logger实例，如果参数为空则返回root logger
    logger = logging.getLogger(name)

    # 指定日志的最低输出级别
    logger.setLevel(level)

    # 控制台日志
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)

    # 为logger添加的日志处理器
    logger.addHandler(ch)

    return logger


logger = init_stdout_logger('yonder')

