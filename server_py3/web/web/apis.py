#!/usr/bin/env python3

import ujson
from . import app
from .models import User
from .consts import RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from sim.exceptions import abort

ERROR_CODE = -1


def html_escape(s):
    r = s.replace('&', '&amp;') \
         .replace('>', '&gt;')  \
         .replace('<', '&lt;')  \
         .replace("'", '&#39;') \
         .replace('"', '&#34;')
    return r


def is_ascii(s):
    return len(s) == len(s.encode())


def valid_username(name):
    assert isinstance(name, str)
    if ' ' in name:
        abort(ERROR_CODE, "username can not contain blank space")

    if not (4 <= len(name) <= 20):
        abort(ERROR_CODE, "username len must between 4 and 20")

    # prevent xss
    valid_name = html_escape(name)
    if valid_name != name:
        abort(ERROR_CODE, "username can not contain html special char")

    # if not is_ascii(user.name):
    #     abort(ERROR_CODE, "no-ascii char is not supported for username yet")

    # if not re.match(r"^[a-zA-Z\_][0-9a-zA-Z\_]{3, 19}$", user.name):
    # app.logger.error(f"re not match for username: {user.name}")
    # abort(ERROR_CODE, "username is invalid")

    return name


def valid_password(password):
    if ' ' in password:
        abort(ERROR_CODE, "password can not contain blank space")

    if not (3 <= len(password) <= 20):
        abort(ERROR_CODE, "password len must between 3 and 20")

    if not is_ascii(password):
        abort(ERROR_CODE, "password can not contain no-ascii char")

    return password


@app.route('/api/user/signup', methods=('POST', ))
def singup(ctx):
    input_json = ctx.request.json()
    if not input_json or "username" not in input_json or 'password' not in input_json:
        abort(ERROR_CODE, "username and password are required")

    username = valid_username(input_json['username'])
    password = valid_password(input_json['password'])

    # check if user existed
    if User.find_by_name(username) is not None:
        abort(ERROR_CODE, f"user `{username}` existed")

    user = User()
    user.name = username
    user.password = user.gen_password_hash(password)
    user.status = USER.status.active
    user.role_id = USER.role.user
    # user.role = user.get_role()

    user.save()
    if getattr(user, 'id', None) is None:
        abort(ERROR_CODE, "create new user error")

    return user.without_password()


@app.route('/api/user/:uid')
def get_user(ctx):
    # req = ctx.request
    uid = ctx.request.get_param('uid')
    try:
        uid = int(uid)
    except Exception as e:
        app.logger.error(f"uid must be an integer, but get uid: {uid}")
        abort(ERROR_CODE, "uid must be an integer")

    user = User.find(uid)
    if not user:
        abort(ERROR_CODE, "user not found")

    return user.without_password()


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
