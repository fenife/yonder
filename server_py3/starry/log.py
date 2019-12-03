#!/usr/bin/env python3

import sys
import logging


def init_stdout_logger(name, level=logging.ERROR):
    # 指定logger输出格式
    # fmt = "\n[%(asctime)s]-[%(levelname)-5s]-[%(filename)s:%(funcName)s:%(lineno)d]:: %(message)s"
    fmt = "\n%(asctime)s||lv=%(levelname)-5s||f=%(filename)s||func=%(funcName)s||line=%(lineno)d:: %(message)s"
    # fmt = "\n%(asctime)s|%(levelname)-5s|%(filename)s|%(funcName)s|%(lineno)d:: %(message)s"

    # 获取logger实例，如果参数为空则返回root logger
    logger = logging.getLogger(name)
    formatter = logging.Formatter(fmt, datefmt='%Y-%m-%d %H:%M:%S')

    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值

    # 为logger添加的日志处理器
    logger.addHandler(console_handler)

    # 指定日志的最低输出级别，默认为INFO级别
    logger.setLevel(level)

    return logger


# 目前输出到stdout，可通过重定向`>`输出到文件中
logger = init_stdout_logger(__name__)
