#!/usr/bin/env python3

from sim.context import AppRequestContext
from wes.api._utils import to_int


def get_cid_from_request(ctx: AppRequestContext):
    # cid: category id
    cid = ctx.request.get_param('cid')      # 动态路由参数
    if not cid:
        cid = ctx.request.get_uri_arg('cid')        # url中?后面的参数

    cid = to_int('cid', cid)

    return cid
