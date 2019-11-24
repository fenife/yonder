#!/usr/bin/env python3

import MySQLdb

from .exceptions import AppBaseException
from .settings import app_configs


#
# db exceptions
#


class DBConfigError(AppBaseException):
    code = -100


class DBConnectError(AppBaseException):
    code = -110


class DBCloseError(AppBaseException):
    code = -120


class DBError(AppBaseException):
    code = -130


#
# db config
#

class DbConfig(object):
    def __init__(self, name):
        self.name = name
        self.dbInfo = self.get_config()

        try:
            self.host = self.dbInfo['host']
            self.user = self.dbInfo['user']
            self.password = self.dbInfo['password']
            self.database = self.dbInfo['db']
            self.port = int(self.dbInfo['port']) if 'port' in self.dbInfo else 3306
            self.charset = self.dbInfo['charset'] if 'charset' in self.dbInfo else "utf8"

        except TypeError:
            raise DBConfigError

    def get_config(self):
        conf = app_configs.get("mysql", {}).get(self.name)
        if not conf:
            print(f"can not get db config: {self.name}")
            raise DBConfigError

        return conf


#
# db loader
#


class Database(object):
    def __init__(self, name):
        self.name = name
        self.dbConf = DbConfig(self.name)
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            self.conn = MySQLdb.connect(
                host=self.dbConf.host,
                port=self.dbConf.port,
                user=self.dbConf.user,
                password=self.dbConf.password,
                db=self.dbConf.database,
                charset=self.dbConf.charset,
                connect_timeout=10
            )

            self.conn.autocommit(True)      # 自动提交事务

            self.cur = self.conn.cursor(MySQLdb.cursors.DictCursor)

        except Exception as e:
            print(e)
            raise DBConnectError

    def close(self):
        try:
            self.cur.close()
            self.conn.close()
            self.cur = None
            self.conn = None
        except Exception as e:
            print(e)
            raise DBConnectError

    def select(self, sql, size=None):
        if not self.cur:
            self.connect()

        print(f"SELECT: {sql}")

        try:
            self.cur.execute(sql)
            if size:
                data = self.cur.fetchmany(size)
            else:
                data = self.cur.fetchall()

        except Exception as e:
            print(e)
            # data = None
            raise DBError

        print(f"rows returned: {len(data)}")
        return data

    def execute(self, sql):
        if not self.cur:
            self.connect()

        print(f"EXECUTE: {sql}")

        try:
            ret = self.cur.execute(sql)
            return ret

        except Exception as e:
            print(e)
            return False


#
# db query and execute
# connect to database everytime
# todo: connection pool
#


class ConnContextManager(object):
    default_dbname = 'test'

    def __init__(self, dbname=None):
        self.dbName = dbname or self.default_dbname
        self.dbConf = DbConfig(self.dbName)
        self.conn = None

    def __enter__(self):
        self.conn = MySQLdb.connect(
            host=self.dbConf.host,
            port=self.dbConf.port,
            user=self.dbConf.user,
            password=self.dbConf.password,
            db=self.dbConf.database,
            charset=self.dbConf.charset,
            connect_timeout=10
        )

        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


def select(sql, size=None):
    print(f"[SELECT] - {sql}")

    with ConnContextManager() as conn:
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(sql)
        if size:
            data = cur.fetchmany(size)
        else:
            data = cur.fetchall()

        cur.close()

        print(f"rows returned: {len(data)}")
        return data


def execute(sql, args=None, autocommit=True):
    print(f"[EXECUTE] - {sql}")

    with ConnContextManager() as conn:
        if not autocommit:
            conn.begin()

        try:
            cur = conn.cursor()
            cur.execute(sql, args)
            affected = cur.rowcount
            cur.close()

            if not autocommit:
                conn.commit()

        except Exception as e:
            if not autocommit:
                conn.rollback()

            raise

        return affected


#
# orm
#


class Field(object):
    def __init__(self, name, column_type, primary_key=False, default=None, null=True, comment=None):
        # name, type, size, decimal, allowNULL, isKey, comment,
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
        self.null = null
        self.comment = comment

    def __str__(self):
        return f"<{self.__class__.__name__}, {self.column_type}:{self.name}>"


class VarcharField(Field):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class IntField(Field):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class Model(object):
    pass


#
# test
#


def _test():
    # c = DbConfig('test')
    # print(c.dbInfo)

    # db = Database('test')
    # print(db.dbConf.dbInfo)

    from .pretty import dictList2Table

    sql = "select * from t1"
    # data = db.select(sql)
    data = select(sql)
    print(dictList2Table(data))

    sql = "desc t1"
    data = select(sql)
    print(dictList2Table(data))


if __name__ == "__main__":
    _test()
