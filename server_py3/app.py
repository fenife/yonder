#!/usr/bin/env python3

import json
from starry.application import Application
from starry.norm import (DBTest, Model, IntField, VarcharField)
from starry.response import Response
from starry.exceptions import Unauthorized
from starry.log import logger

app = Application()


class User(Model):
    id = IntField(column_type='int', null=False, primary_key=True, extra="auto_increment")
    name = VarcharField(column_type='varchar(255)')
    # name = VarcharField(column_type='varchar(255)', primary_key=True)

    __database__ = DBTest
    __table__ = 'users'
    __unique_key__ = ('id', 'name')
    __index_key__ = [('id', 'name'), ('name',)]


@app.before_request
def before_req(ctx):
    # print('before_req:', ctx.request.path)
    logger.info(f"before_req: {ctx.request.path}")


@app.after_request
def after_req(ctx, response):
    print('after_req:', ctx.request.path, response.status_code)
    return response


def login_required(func):
    """login required"""
    def decorator(ctx):
        if not getattr(ctx, 'user', None):
            raise Unauthorized()

        return func(ctx)

    return decorator


@app.route('/')
def index(ctx):
    resp = {'a': 1, 'b': 2}
    resp = json.dumps(resp).encode()
    # resp = Response(data=b"hello yonder")
    # return resp
    return None


@app.route('/user/:id')
@login_required
def get_user(ctx):
    params = ctx.request.params
    query = ctx.request.all_query()
    data = {
        "params": params,
        "query": query,
    }
    print("data:", data)
    # resp = Response(data=data)
    return data


@app.route('/users/')
def users(ctx):
    sql = "select * from users"
    req = ctx.request
    data = User.select(sql)
    req_body = ctx.request.json()
    query = ctx.request.all_query()
    cookies = ctx.request.cookies

    result = {
        "users": data,
        "req_body": req_body,
        "query": query,
        "cookies": cookies,
    }
    # print(result)

    return result


@app.route('/test/cookies')
def test_cookie(ctx):
    ctx.set_cookie(name='a', value=1)
    ctx.set_cookie(name='b', value=2)

    result = {}
    for k, c in ctx.cookies.items():
        v = c.output()
        result[k] = v

    return result


def _test_orm():
    """
    CREATE TABLE `users` (
      `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
      `name` varchar(255) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    insert into users (`name`) values ("u1");
    """
    from starry.pretty import dictList2Table

    print(User.__table__)
    print(User.__mappings__)

    # sql = "select * from users"
    # data = User.select(sql)
    # print(dictList2Table(data))

    # User.create()

    print()
    sql = "desc users"
    data = User.select(sql)
    print(dictList2Table(data))


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
    _test()
    # _test_orm()
