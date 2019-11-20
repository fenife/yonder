#!/usr/bin/env python3

import json
from starry.application import Application

app = Application()


@app.route('/')
def index(ctx):
    data = {'a': 1, 'b': 2}
    resp = {
        "code": 200,
        "data": data,
        "msg": "success"
    }
    # resp = json.dumps(resp).encode()
    # resp = b"hello yonder"
    return resp


@app.route('/user/:id')
def view_tree(ctx):
    params = ctx.params
    return params


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
