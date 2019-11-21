#!/usr/bin/env python3

import MySQLdb

from .exceptions import (DBConfigError, DBConnectError,)

app_configs = {
    "mysql": {
        # dbName, connect config
        "test": {
            "host": '127.0.0.1',
            "port": 3306,
            "user": "test",
            "password": "test",
            "db": "test",
            "charset": "utf8",
        }
    },
}


class DbConfig(object):
    def __init__(self, name):
        self.name = name
        self.conf = self.get_config()

    def get_config(self):
        conf = app_configs.get("mysql", {}).get(self.name)
        if not conf:
            print(f"can not get db config: {self.name}")
            raise DBConfigError

        return conf


class Database(object):
    def __init__(self, name):
        self.name = name
        self.conn = None
        self.cur = None
        self.conf = None



    def connect(self):
        self.conn = MySQLdb.connect(
            host=self.dbConf.host,
            port=self.dbConf.port,
            user=self.dbConf.user,
            passwd=self.dbConf.passwd,
            db=self.dbConf.database,
            charset=self.dbConf.charset,
            connect_timeout=10
        )

    def close(self):
        pass

    def select(self):
        pass

    def execute(self):
        pass


class Model(object):
    pass


class Field(object):
    pass


