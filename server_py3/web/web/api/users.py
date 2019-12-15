#!/usr/bin/env python3

from sim.exceptions import abort
from .. import app, db, cache_pool
from ..model import User
from ..consts import RespCode, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from ..decorators import login_required


@app.route('/api/user/signup', methods=('POST', ))
def singup(ctx):
    """用户注册"""
    input_json = ctx.request.json()
    if not input_json or "username" not in input_json or 'password' not in input_json:
        abort(RespCode.error, "username and password are required")

    username = User.valid_username(input_json['username'])
    password = User.valid_password(input_json['password'])

    # check if user existed
    if User.find_by_name(username) is not None:
        abort(RespCode.error, f"username `{username}` existed")

    user = User()
    user.name = username
    user.password = user.gen_password_hash(password)
    user.status = USER.status.active
    user.role_id = USER.role.user
    # user.role = user.get_role()

    user.save()
    if getattr(user, 'id', None) is None:
        abort(RespCode.error, "create new user error")

    return user.without_password()


@app.route('/api/user/signin', methods=('POST', ))
def signin(ctx):
    """用户登录"""
    input_json = ctx.request.json()
    if not input_json or "username" not in input_json or 'password' not in input_json:
        abort(RespCode.error, "username and password are required")

    username = User.valid_username(input_json['username'])
    password = User.valid_password(input_json['password'])

    # 查找用户
    user = User.find_by_name(username)
    # 检查用户是否存在或是否已删除
    if user is None or user.status != USER.status.active:
        abort(RespCode.error, "user not found")

    # 检查密码是否错误
    if not user.verify_password(password):
        abort(RespCode.error, "password is not correct")

    # gen cookie token
    token = user.gen_session_token()

    # set-cookie
    ctx.set_cookie(name='token', value=token, max_age=10)       # todo: reset max_age

    # save to redis
    User.save_user_to_redis_by_token(user, token)

    return user.without_password()


@app.route('/api/user/info')
@login_required()
def get_user_info(ctx):
    user = ctx.user
    assert isinstance(user, User)
    return user.without_password()


@app.route('/api/user/:uid')
def get_user(ctx):
    uid = ctx.request.get_param('uid')
    try:
        uid = int(uid)
    except Exception as e:
        app.logger.error(f"uid must be an integer, but get uid: {uid}")
        abort(RespCode.error, "uid must be an integer")

    user = User.find(uid)
    if not user:
        abort(RespCode.error, "user not found")

    return user.without_password()


@app.route('/api/user/:uid', methods=('PUT', ))
@login_required()
def update_user(ctx):
    uid = ctx.request.get_param('uid')
    try:
        uid = int(uid)
    except Exception as e:
        app.logger.error(f"uid must be an integer, but get uid: {uid}")
        abort(RespCode.error, "uid must be an integer")

    user = ctx.user
    assert isinstance(user, User)
    if user.id != uid and not user.is_admin():
        app.logger.error(f"not the owner, uid({user.id}) != user.id({user.id})")
        abort(RespCode.error, 'permission denied')

    # todo:
    input_json = ctx.request.json()
    if not input_json:
        abort(RespCode.error, "body data required")

    supported = {'username', }
    unsupported = set(input_json.keys()) - supported
    if unsupported:
        abort(RespCode.error, f"unsupported fields: {list(unsupported)}")

    need_update = False
    if 'username' in input_json:
        username = input_json.pop('username')

        # username need update
        if username != user.name:
            username = User.valid_username(username)
            # check if user existed
            if User.find_by_name(username) is not None:
                abort(RespCode.error, f"username `{username}` existed")

            user.name = username
            need_update = True
        else:
            abort(RespCode.error, f"username `{username}` is the same as before")

    if need_update:
        if user.modify():
            # 清除相关缓存，重新登录
            token = ctx.request.get_cookie('token')
            user.del_user_in_redis(token)

    return user

