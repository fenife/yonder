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


class DBTest(Database):
    """
    database: test
    """
    @classmethod
    def select(cls, sql, *args, **kwargs):
        return select(sql, *args, **kwargs)

    @classmethod
    def execute(cls, sql, *args, **kwargs):
        return execute(sql, *args, **kwargs)


class Field(object):
    def __init__(self, name=None, column_type=None, primary_key=False, default=None, null=True, comment=None):
        # name, type, size, decimal, allowNULL, isKey, comment,
        self.name = name

        if not column_type:
            raise Exception("column type is missed")

        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
        self.null = null
        self.comment = comment

    def sql_for_create(self):
        sql = ""
        if not self.column_type:
            raise Exception("column type is missed")

        if self.column_type:
            sql += f" {self.column_type}"

        if not self.null:
            sql += " NOT NULL"

        if self.default:
            sql += f"  DEFAULT {self.default}"
        else:
            sql += f"  DEFAULT NULL"

        if self.comment:
            sql += f"  COMMENT {self.default}"

        return sql

    def __str__(self):
        return f"<{self.__class__.__name__}, {self.column_type}>"


class VarcharField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class IntField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        # print(cls)
        # print("name:", name)
        # print("bases:", bases)
        # print("attrs:")
        # for k, v in attrs.items():
        #     print(k, ":", v)
        # print()

        if '__database__' not in attrs:
            raise Exception('__database__ is missed')

        if '__table__' not in attrs:
            raise Exception('__table__ is missed')

        mappings = dict()
        fields = list()
        primary_key = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                # print(f"    mapping: {k} ==> {v}")
                mappings[k] = v
                if v.primary_key:
                    if primary_key:
                        raise Exception(f"Duplicate primary key for `{k}`")

                    primary_key = k

                fields.append(k)

        if not primary_key:
            raise Exception("primary key not found")

        for k in mappings.keys():
            attrs.pop(k)

        escaped_fields = list(map(lambda f: f"`{f}`", fields))
        attrs['__mappings__'] = mappings
        attrs['__fields__'] = fields
        attrs['__escaped_fields__'] = escaped_fields
        attrs['__primary_key__'] = primary_key

        print()
        for k, v in attrs.items():
            print(k, ":", v)

        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"`Model` object has no attrbute `{item}`")

    def __setattr__(self, key, value):
        self[key] = value

    @classmethod
    def migrate(cls):
        pass

    @classmethod
    def create(cls):
        for name, field in cls.__mappings__.items():
            assert isinstance(field, Field), f"field: {field}"
            print(f"`{name}`: '{field.sql_for_create()}'")

    @classmethod
    def select(cls, sql, *args, **kwargs):
        db = cls.__database__
        assert issubclass(db, Database)

        return db.select(sql, *args, **kwargs)

    @classmethod
    def execute(cls, sql, *args, **kwargs):
        db = cls.__database__
        assert issubclass(db, Database)

        return db.select(sql, *args, **kwargs)


#
# test
#


def _test_orm():
    """
        CREATE TABLE IF NOT EXISTS `users` (
          `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
          `name` varchar(255) NOT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

        insert into users (`name`) values ("u1");
        """
    from .pretty import dictList2Table

    class User(Model):
        id = IntField(column_type='int', primary_key=True)
        name = VarcharField(column_type='varchar(255)')
        # name = VarcharField(column_type='varchar(255)', primary_key=True)

        __database__ = DBTest
        __table__ = 'users'

    print(User.__table__)
    print(User.__mappings__)

    sql = "select * from users"
    data = User.select(sql)
    print(dictList2Table(data))

    User.create()


def _test():
    from .pretty import dictList2Table

    # c = DbConfig('test')
    # print(c.dbInfo)

    # db = Database('test')
    # print(db.dbConf.dbInfo)

    sql = "select * from users"
    # data = db.select(sql)
    data = select(sql)
    print(dictList2Table(data))

    print()
    sql = "desc users"
    data = select(sql)
    print(dictList2Table(data))


if __name__ == "__main__":
    # _test()
    _test_orm()
