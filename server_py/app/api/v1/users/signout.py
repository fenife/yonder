#!/usr/bin/env python3

from lime.context import AppRequestContext
from app.model import User
from app.api.decorators import login_required
from app.api.desc import ApiDescBase, api_desc_wrapper
from .. import api_group


@api_group.route('/user/signout')
@login_required()
def signout(ctx: AppRequestContext):
    """用户退出"""
    token = ctx.request.get_cookie('token')
    user = ctx.user
    if isinstance(user, User):
        user.del_user_from_redis(token)


@api_group.route('/user/signout/desc', methods=('GET', ))
@api_desc_wrapper()
class ApiSignoutDesc(ApiDescBase):
    name = "用户退出"
    desc = ""
    method = ['GET']
    rule = "/api/user/signout"

    def req_headers(self):
        headers = [
            # (key, val, desc)
            ('Cookie', 'token=xxx', "用户登录token"),
        ]
        return headers

    @property
    def example(self):
        r = {
            "url": self.url,
            "request": {
                "headers": {
                    "Cookie": {
                        "value": "token=334a9d0...",
                    }
                }
            },
            "response": {
                "code": 0,
                "data": None,
                "msg": "OK"
            }
        }
        return r

