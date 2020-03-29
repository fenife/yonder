#!/usr/bin/env python3

import sys
import os
import logging
from sim.application import Application
from sim.log import setup_logger, LoggerManager

YONDER_HOME = os.path.abspath(__file__).split('/src', 1)[0]
CONF_FILE   = f"{YONDER_HOME}/etc/server/yonder.conf"

with open(CONF_FILE, 'r') as f:
    configs = eval(f.read())

DEBUG_MODE = True if configs.get('DEBUG_MODE') else False

print()
print('-' * 50)
print(f" conf file : {CONF_FILE}")
print(f"  env mode : {configs['ENV_MODE']}")
print(f"debug mode : {DEBUG_MODE}")
print('-' * 50)
print()


class AppConfig(object):
    log_level = logging.DEBUG if DEBUG_MODE else logging.INFO
    configs = configs

    @classmethod
    def init_app(cls, app: Application):
        app.update_config(cls.configs)

        lgm = LoggerManager(
            [app.logger, logging.getLogger('sim')],
            cls.log_level,
        )
        lgm.addConsoleHandler()
        log_file = cls.configs['LOG_FILE']
        lgm.addTimedFileHandler(filename=log_file, backupCount=30)
