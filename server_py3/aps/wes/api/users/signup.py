#!/usr/bin/env python3

from sim.exceptions import abort
from sim.context import AppRequestContext
from ... import app, db, cache_pool
from ...model import User
from ...consts import RespCode, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from ...decorators import login_required
from ...desc import ApiDescBase, api_desc_wrapper
from .. import api_group


@api_group.route('/user/signup', methods=('POST', ))
def singup(ctx: AppRequestContext):
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

    # 密码需要加密为hash字符串后保存
    # 不保存明文密码
    user.password = user.gen_password_hash(password)

    user.status = USER.status.active
    user.role_id = USER.role.user
    # user.role = user.get_role()

    user.save()
    if getattr(user, 'id', None) is None:
        abort(RespCode.error, "create new user error")

    return user.without_password()


@api_group.route('/user/signup/desc', methods=('POST', ))
@api_desc_wrapper()
class ApiSignupDesc(ApiDescBase):
    name = "用户注册"
    desc = ""
    method = ['POST']
    rule = "/api/user/signup"

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
            "url": self.url,
            "request": {
                "body": {
                    "username": "aabb",
                    "password": "aabb"
                }
            },
            "response": {
                "code": 0,
                "data": {
                    "name": "aabb",
                    "status": 1,
                    "role_id": 2,
                    "created_at": "2020-01-13 21:30:58",
                    "updated_at": "2020-01-13 21:30:58",
                    "id": 2
                },
                "msg": "OK"
            }
        }
        return r

