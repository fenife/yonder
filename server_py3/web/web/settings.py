#!/usr/bin/env python3


_dev_configs = {
    # database config
    "DB_HOST": '127.0.0.1',
    "DB_PORT": 3306,
    "DB_USER": "test",
    "DB_PASSWORD": "test",
    "DB_NAME": "test",
    "DB_CHARSET": "utf8",
}


configs = {
    'default': _dev_configs,
    'dev': _dev_configs,
}
