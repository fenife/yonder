#!/usr/bin/env python3

import hashlib
from sim.context import AppRequestContext
from wes.api._utils import to_int


def content_hash(content: str):
    """计算文章内容的hash，用于对比更新前后内容是否有改变"""
    if not content:
        return

    m = hashlib.md5()
    m.update(content.encode('utf-8'))
    h = m.hexdigest()
    return h


def get_aid_from_request(ctx: AppRequestContext):
    # aid: article id
    aid = ctx.request.get_param('aid')      # 动态路由参数
    if not aid:
        aid = ctx.request.get_uri_arg('aid')        # url中?后面的参数

    aid = to_int('aid', aid)

    return aid
