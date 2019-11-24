#!/usr/bin/env python3

import json
from starry.application import Application
from starry.norm import (DBTest, Model, IntField, VarcharField)

app = Application()


@app.route('/')
def index(ctx):
    resp = {'a': 1, 'b': 2}
    # resp = json.dumps(resp).encode()
    resp = b"hello yonder"
    return resp


@app.route('/user/:id')
def view_tree(ctx):
    params = ctx.params
    query = ctx.query
    data = {
        "params": params,
        "query": query,
    }
    print("data:", data)
    return data


def _test_orm():
    """
    CREATE TABLE IF NOT EXISTS `users` (
      `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
      `name` varchar(255) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    insert into users (`name`) values ("u1");
    """
    from starry.pretty import dictList2Table

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
    # app = Application()
    host = '0.0.0.0'
    port = 6070
    app.run(host=host, port=port)


def _test1():
    class Response(object):
        def __init__(self, a=None, b=None):
            self.a = a or 1
            self.b = b or 2

        def __call__(self, *args, **kwargs):
            return self.a + self.b

    resp = Response()
    print(resp())


if __name__ == "__main__":
    # _test()
    _test_orm()
