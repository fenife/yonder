#!/usr/bin/env python3

from sim.context import AppRequestContext
from sim.exceptions import abort
from ...consts import RespCode
from .._utils import to_int


def get_uid_from_request(ctx: AppRequestContext):
    # uid: user id
    uid = ctx.request.get_param('uid')      # 动态路由参数
    if not uid:
        uid = ctx.request.get_uri_arg('uid')        # url中?后面的参数

    uid = to_int('uid', uid)

    return uid
