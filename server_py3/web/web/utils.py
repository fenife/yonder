#!/usr/bin/env python3

import json
from . import app, db, cache_pool
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


def save_user_to_redis_by_token(user, token):
    assert isinstance(user, User)
    with cache_pool.get() as cache:
        key = f"token:{token}"
        val = json.dumps(user, default=str).encode('utf-8')
        cache.set(key, val, ex=USER.login_expired)


def load_user_from_redis_by_token(token):
    with cache_pool.get() as cache:
        key = f"token:{token}"
        val = cache.get(key)
        if not val:
            return

        data = json.loads(val)
        user = User(**data)
        return user
