#!/usr/bin/env python3

import ujson
from . import app
from .models import User
from sim.exceptions import abort


@app.route('/')
def index(ctx):
    resp = "hello web"
    return resp


@app.route('/obj')
def index(ctx):
    resp = {'a': 1, 'b': 2}
    resp = [1, 2, 3, 4, 5]
    return resp


@app.route('/bytes')
def test_bytes(ctx):
    resp = {'a': 1, 'b': 2}
    resp = [1, 2, 3, 4, 5]
    resp = ujson.dumps(resp).encode()
    return resp


@app.route('/user/:id')
def user(ctx):
    try:
        uid = int(ctx.request.get_param('id'))
    except Exception as e:
        app.logger.error("param uid invalid, uid must be an integer")
        abort(-1, "uid must be an integer")

    user = User.get_user(uid)
    if not user:
        abort(-1, "user not exist")

    return user
