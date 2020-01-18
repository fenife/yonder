#!/usr/bin/env python3

from sim.exceptions import abort
from sim.context import AppRequestContext
from ... import app, db, cache_pool
from ...model import User
from ...consts import RespCode, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from ...decorators import login_required
from ...desc import ApiDescBase, api_desc_wrapper
from .. import api_group
from ._internal import get_uid_from_request


@api_group.route('/user/update', methods=('PUT', ))
@login_required()
def update_user(ctx):
    """用户更新"""
    # uid = ctx.request.get_param('uid')
    # try:
    #     uid = int(uid)
    # except Exception as e:
    #     app.logger.error(f"uid must be an integer, but get uid: {uid}")
    #     abort(RespCode.error, "uid must be an integer")

    uid = get_uid_from_request(ctx)

    user = ctx.user
    assert isinstance(user, User)
    if user.id != uid and not user.is_admin():
        app.logger.error(f"not the owner, uid({user.id}) != user.id({user.id})")
        abort(RespCode.error, 'permission denied')

    input_json = ctx.request.json()
    if not input_json:
        abort(RespCode.error, "body data required")

    supported = {'username', 'password'}
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

    if 'password' in input_json:
        password = input_json.pop('password')
        password = User.valid_password(password)
        if user.verify_password(password):
            abort(RespCode.error, f"password is the same as before")

        # 有cookie说明登录成功，则不用验证旧密码了，直接更新密码
        user.password = user.gen_password_hash(password)
        need_update = True

    if need_update:
        if user.modify():
            # 清除相关缓存，重新登录
            token = ctx.request.get_cookie('token')
            user.del_user_from_redis(token)

    return user.without_password()


@api_group.route('/user/update/desc', methods=('PUT', ))
@api_desc_wrapper()
class ApiCateCreateDesc(ApiDescBase):
    name = "用户更新"
    desc = ""
    method = ['PUT']
    rule = "/api/user/update"

    def req_headers(self):
        headers = [
            # (key, val, desc)
            ('Cookie', 'token=xxx', "用户登录token"),
        ] + self.default_req_headers
        return headers

    def req_args(self):
        args = [
            # (key, name, type, default, required, desc)
            # (字段，字段名称，字段类型，默认值，是否必传，备注描述)
            ('uid', '用户ID', 'number', '', 1, ''),
        ]
        return args

    def req_body(self):
        # {
        # 	"username": "aabb",
        # 	"password": "aabb"
        # }
        body = [
            # (key, name, type, default, required, desc)
            ('username', '用户名称', 'string', '', 1, '名称长度为4~20个字符，不能包含空格等特殊字符'),
            ('password', '用户密码', 'string', '', 1, '长度3~20个字符，只能是ascii字符，且不能包含空格等特殊字符'),
        ]
        return body

    @property
    def example(self):
        r = {
            "url": self.url + '?uid=2',
            "request": {
                "body": {
                    "username": "aabbb",
                    "password": "aabbb"
                }
            },
            "response": {
                "code": 0,
                "data": {
                    "id": 2,
                    "created_at": "2020-01-18 10:39:57",
                    "updated_at": "2020-01-18 10:47:05",
                    "name": "aabbb",
                    "role_id": 2,
                    "status": 1
                },
                "msg": "OK"
            }
        }
        return r

