#!/usr/bin/env python3

import sys
import os
import json
import logging
from lime.application import Application
from lime.log import setup_logger, LoggerManager

from . import server_path

CONF_FILE   = f"{server_path}/config/server.json"

with open(CONF_FILE, 'r') as f:
    configs = json.load(f)

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
        log_file = f"{cls.configs['LOG_PATH']}/server_py3/aps/wes.log"
        lgm.addTimedFileHandler(filename=log_file, backupCount=30)
