#!/usr/bin/env python3

import hashlib
import markdown
from sim.context import AppRequestContext
from sim.exceptions import abort
from ...consts import RespCode
from .._utils import to_int


def content_hash(content):
    """计算文章内容的hash，用于对比更新前后内容是否有改变"""
    if not content:
        return

    m = hashlib.md5()
    m.update(content.encode('utf-8'))
    h = m.hexdigest()
    return h


def get_aid_from_request(ctx):
    # aid: article id
    aid = ctx.request.get_param('aid')
    aid = to_int('aid', aid)

    return aid
