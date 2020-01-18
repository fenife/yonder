#!/usr/bin/env python3

from sim.exceptions import abort
from sim.context import AppRequestContext
from ... import app, db, cache_pool
from ...model import User
from ...consts import RespCode, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from ...decorators import login_required
from ...desc import ApiDescBase, api_desc_wrapper
from .. import api_group


@api_group.route('/user/info')
@login_required()
def get_user_info(ctx):
    """登录用户的信息"""
    user = ctx.user
    assert isinstance(user, User)
    return user.without_password()


@api_group.route('/user/info/desc', methods=('GET', ))
@api_desc_wrapper()
class ApiCateCreateDesc(ApiDescBase):
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

