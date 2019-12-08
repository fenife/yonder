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
        # self.conn.autocommit(True)  # 自动提交事务

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

    def select(self, sql, args=None, size=None):
        has_args = False
        if sql.find('?') > 0:
            has_args = True

        if has_args:
            sql = sql.replace('?', '%s')

        print(f"[SELECT] - {sql}, {args}")

        with ConnContextManager(self) as conn:
            cur = conn.cursor(MySQLdb.cursors.DictCursor)

            if has_args:
                cur.execute(sql, args)
            else:
                cur.execute(sql)

            if size:
                data = cur.fetchmany(size)
            else:
                data = cur.fetchall()

            cur.close()

            print(f"rows returned: {len(data)}")
            return data

    def execute(self, sql, args=None, autocommit=True):
        if sql.find('?') > 0:
            sql = sql.replace('?', '%s')

        print(f"[EXECUTE] - {sql}")

        with ConnContextManager(self) as conn:
            if not autocommit:
                conn.autocommit(False)
                conn.begin()
            else:
                conn.autocommit(True)  # 自动提交事务

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

        if self.default and not callable(self.default):
            # 如果default是可调用的函数，则后面保存时会自动调用此函数生成值
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

        table_name = attrs['__table__']
        mappings = dict()
        fields = list()
        primary_key = None

        # 主键是否是自增id
        # 如果是，后面insert时生成的sql就不必带有primary_key
        pk_auto_increment = False

        for k, v in attrs.items():
            if isinstance(v, Field):
                # print(f"    mapping: {k} ==> {v}")
                mappings[k] = v
                if v.primary_key:
                    if primary_key:
                        raise Exception(f"Duplicate primary key for `{k}`")

                    primary_key = k
                    if v.extra == 'auto_increment':
                        pk_auto_increment = True            # 主键是自增id
                else:
                    fields.append(k)

        if not primary_key:
            raise Exception("primary key not found")

        for k in mappings.keys():
            attrs.pop(k)

        escaped_fields = list(map(lambda f: f"`{f}`", fields))
        attrs['__mappings__'] = mappings            # 保存属性和列的映射关系
        attrs['__fields__'] = fields                # 除主键外的属性名
        attrs['__primary_key__'] = primary_key      # 主键的属性名
        attrs['__pk_auto_increment__'] = pk_auto_increment      # 主键是否是自增id
        # attrs['__escaped_fields__'] = escaped_fields

        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primary_key, ', '.join(escaped_fields), table_name)

        if pk_auto_increment:
            # 主键是自增id，insert时不必带上主键
            attrs['__insert__'] = 'insert into `%s` (%s) values (%s)' % (
                table_name, ', '.join(escaped_fields),
                ','.join(['?'] * len(escaped_fields)),        # eg: ?,?,?
            )
        else:
            # 主键是非自增id，insert时要带上主键
            attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (
                table_name, ', '.join(escaped_fields), primary_key,
                ','.join(['?'] * (len(escaped_fields) + 1)),        # eg: ?,?,?
            )

        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (
            table_name,
            ', '.join(map(lambda f: '`%s`=?' % f, fields)),     # eg: `name`=?, `password`=?, `role`=?
            primary_key,
        )

        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (table_name, primary_key)

        logger.debug(f"show model attrs:")
        for k, v in attrs.items():
            print(f"{k:>24s} : {v}")
        print()

        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"`Model` object has no attribute `{item}`")

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
    __pk_auto_increment__ = False
    __mappings__ = dict()
    __fields__ = list()

    @classmethod
    def migrate(cls):
        pass

    @classmethod
    def table_create(cls):
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

        assert isinstance(cls.__database__, Database)
        return cls.__database__.execute(sql)

    @classmethod
    def table_drop(cls):
        sql = f"drop table {cls.__table__}"
        print(sql)

        assert isinstance(cls.__database__, Database)
        return cls.__database__.execute(sql)

    @classmethod
    def find(cls, pk):
        sql = f"{cls.__select__} where `{cls.__primary_key__}`=?"
        data = cls.__database__.select(sql, [pk], 1)
        if not data:
            return None
        return cls(**data[0])

    def get_value(self, key):
        return getattr(self, key, None)

    def get_value_or_default(self, key):
        val = getattr(self, key, None)
        if val is None:
            field = self.__mappings__[key]
            assert isinstance(field, Field)
            if field.default is not None:
                val = field.default() if callable(field.default) else field.default
                logger.debug(f"using default value for {key}: {str(val)}")
                setattr(self, key, val)

        return val

    def save(self):
        args = list(map(self.get_value_or_default, self.__fields__))
        if not self.__pk_auto_increment__:
            args.append(self.get_value_or_default(self.__primary_key__))

        print(f"args: {args}")
        rows = self.__database__.execute(self.__insert__, args)
        print(f"rows: {rows}")
        if rows != 1:
            logger.error(f"failed to insert record, affected rows: {rows}")

    def update(self):
        pass

    def remove(self):
        pass
