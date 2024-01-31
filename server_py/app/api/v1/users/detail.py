#!/usr/bin/env python3

from lime.exceptions import abort
from lime.context import AppRequestContext
from app.model import User
from app.consts import RespCode, Permission
from app.api.decorators import permission_required
from app.api.desc import ApiDescBase, api_desc_wrapper
from .. import api_group
from ._internal import get_uid_from_request


@api_group.route('/user/detail')
@permission_required(Permission.admin)
def user_detail(ctx: AppRequestContext):
    """
    用户详情

    本接口可获取所有用户的信息
    但用户信息是私密的，只有管理员有权访问
    """
    uid = get_uid_from_request(ctx)

    user = User.find(uid)
    if not user:
        abort(RespCode.error, "user not found")

    return user.without_password()


@api_group.route('/user/detail/desc', methods=('GET', ))
@api_desc_wrapper()
class ApiUserDetailDesc(ApiDescBase):
    name = "用户详情"
    desc = ""
    method = ['GET']
    rule = "/api/user/detail"

    def req_args(self):
        args = [
            # (key, name, type, default, required, desc)
            # (字段，字段名称，字段类型，默认值，是否必传，备注描述)
            ('uid', '用户ID', 'number', '', 1, ''),
        ]
        return args

    @property
    def example(self):
        r = {
            "url": self.url + '?uid=2',
            "request": {},
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

