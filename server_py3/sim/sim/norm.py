#!/usr/bin/env python3

import MySQLdb
from .log import logger


class ConnContextManager(object):
    def __init__(self, db):
        self.db = db
        self.conn = None

    def __enter__(self):
        self.conn = MySQLdb.connect(
            host=self.db.host,
            port=self.db.port,
            user=self.db.user,
            password=self.db.password,
            db=self.db.db_name,        # database name
            charset=self.db.charset,
            connect_timeout=10
        )

        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


class Database(object):
    def __init__(self, app=None):
        self.app = app
        self.host = None
        self.port = 3306
        self.user = None
        self.password = None
        self.db_name = None
        self.charset = "utf8"

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        from .application import Application
        assert isinstance(app, Application)

        if self.app is None:
            self.app = app

        # "DB_HOST": '127.0.0.1',
        # "DB_PORT": 3306,
        # "DB_USER": "test",
        # "DB_PASSWORD": "test",
        # "DB_NAME": "test",
        # "DB_CHARSET": "utf8",
        self.host = self.app.config["DB_HOST"]
        self.port = self.app.config["DB_PORT"]
        self.user = self.app.config["DB_USER"]
        self.password = self.app.config["DB_PASSWORD"]
        self.db_name = self.app.config["DB_NAME"]
        self.charset = self.app.config["DB_CHARSET"]

    def select(self, sql, size=None):
        print(f"[SELECT] - {sql}")

        with ConnContextManager(self) as conn:
            cur = conn.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(sql)
            if size:
                data = cur.fetchmany(size)
            else:
                data = cur.fetchall()

            cur.close()

            print(f"rows returned: {len(data)}")
            return data

    def execute(self, sql, args=None, autocommit=True):
        print(f"[EXECUTE] - {sql}")

        with ConnContextManager(self) as conn:
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
    def __init__(self, name=None, column_type=None, primary_key=False,
                 default=None, null=True, extra=None, comment=None):
        # name, type, size, decimal, allowNULL, isKey, comment,
        self.name = name

        if not column_type:
            raise Exception("column type is missed")

        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
        self.null = null
        self.extra = extra
        self.comment = comment

    def sql_for_create(self):
        sql = ""
        if not self.column_type:
            raise Exception("column type is missed")

        if self.column_type:
            sql += f" {self.column_type}"

        if not self.null:
            sql += " not null"

        if self.default:
            sql += f" default {self.default}"

        if self.null and not self.default:
            sql += f" default null"

        if self.extra:
            sql += f" {self.extra}"

        if self.comment:
            sql += f" comment {self.default}"

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

        logger.debug(f"show model attrs:")
        for k, v in attrs.items():
            print(f"{k:>20s} : {v}")
        print()

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

    # defined by user
    __database__ = None
    __table__ = None
    __unique_key__ = tuple()
    __index_key__ = list()
    __foreign_key__ = list()    # not support yet

    # filled by norm framework
    __primary_key__ = None
    __mappings__ = dict()
    __fields__ = list()

    @classmethod
    def migrate(cls):
        pass

    @classmethod
    def create(cls):
        """
        CREATE TABLE `users` (
          `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
          `name` varchar(255) NOT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

        :return:
        """
        sql = f"create table `{cls.__table__}` ("

        for name, field in cls.__mappings__.items():
            assert isinstance(field, Field), f"field: {field}"
            # print(f"`{name}`: '{field.sql_for_create()}'")
            sql += f"`{name}`{field.sql_for_create()}, "

        # print(cls.__primary_key__)
        if not cls.__primary_key__:
            raise Exception("primary key not found")

        sql += f"primary key (`{cls.__primary_key__}`)"

        if cls.__unique_key__:
            item = cls.__unique_key__
            assert isinstance(item, (tuple, list)), "unique key item must be a tuple or list"

            key_fields = ','.join(list(map(lambda x: f"`{x}`", item)))
            key_name = f"unique_key_{'_'.join(item)}"
            # sql += f", unique key `{key_name}` ({','.join(escaped_keys)})"
            sql += f", unique key `{key_name}` ({key_fields})"

        if cls.__index_key__:
            for item in cls.__index_key__:
                assert isinstance(item, tuple), "index key item must be a tuple"

                key_fields = ','.join(list(map(lambda x: f"`{x}`", item)))
                key_name = f"key_{'_'.join(item)}"
                # sql += f", key `{key_name}` ({','.join(keys)})"
                sql += f", key `{key_name}` ({key_fields})"

        sql += f") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
        print(sql)

        return cls.execute(sql)

    @classmethod
    def select(cls, sql, *args, **kwargs):
        db = cls.__database__
        assert issubclass(db, Database)

        return db.select(sql, *args, **kwargs)

    @classmethod
    def execute(cls, sql, *args, **kwargs):
        db = cls.__database__
        assert issubclass(db, Database)

        return db.execute(sql, *args, **kwargs)

