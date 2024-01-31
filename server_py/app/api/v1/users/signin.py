#!/usr/bin/env python3

from lime.exceptions import abort
from lime.context import AppRequestContext
from app import app
from app.model import User
from app.consts import RespCode, USER
from app.api.desc import ApiDescBase, api_desc_wrapper
from .. import api_group


@api_group.route('/user/signin', methods=('POST', ))
def signin(ctx: AppRequestContext):
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
    max_age = app.config.get("LOGIN_EXPIRED")
    ctx.set_cookie(name='token', value=token, max_age=max_age)

    # save to redis
    User.save_user_to_redis_by_token(user, token)

    resp = {
        "user": user.without_password(),
        "token": token,
    }

    return resp


@api_group.route('/user/signin/desc', methods=('POST', ))
@api_desc_wrapper()
class ApiSigninDesc(ApiDescBase):
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
            ('username', '用户名称', 'string', '', 1, ''),
            ('password', '用户密码', 'string', '', 1, ''),
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
                    "user": {
                        "id": 2,
                        "created_at": "2020-01-13 21:30:58",
                        "updated_at": "2020-01-13 21:30:58",
                        "name": "aabb",
                        "role_id": 2,
                        "status": 1
                    },
                    "token": "ed46b6c768a95a5a535b23526a36f756"
                },
                "msg": "OK"
            }
        }
        return r

