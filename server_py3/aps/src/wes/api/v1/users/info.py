#!/usr/bin/env python3

from sim.context import AppRequestContext
from wes.model import User
from wes.api.desc import ApiDescBase, api_desc_wrapper
from .. import api_group


@api_group.route('/user/info')
# @login_required()
def get_user_info(ctx: AppRequestContext):
    """登录用户的信息"""
    # 未登陆
    if not getattr(ctx, 'user', None):
        return None

    user = ctx.user
    assert isinstance(user, User)
    return user.without_password()


@api_group.route('/user/info/desc', methods=('GET', ))
@api_desc_wrapper()
class ApiUserInfoDesc(ApiDescBase):
    name = "已登录用户的信息"
    desc = ""
    method = ['GET']
    rule = "/api/user/info"

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
                "data": {
                    "id": 1,
                    "created_at": "2019-12-28 15:11:02",
                    "updated_at": "2019-12-28 15:11:02",
                    "name": "admin",
                    "role_id": 1,
                    "status": 1
                },
                "msg": "OK"
            }
        }
        return r

