#!/usr/bin/env python3

from sim.exceptions import abort
from sim.response import Response
from sim.context import AppRequestContext
from ses import app, cache_pool
from ses.api import api_group
from ses.desc import ApiDescBase, api_desc_wrapper


@api_group.route('/index/update', methods=('POST',))
def update(ctx: AppRequestContext):
    pass


@api_group.route('/index/update/desc', methods=('GET', ))
@api_desc_wrapper()
class ApiAboutDesc(ApiDescBase):
    name = "网站相关"
    desc = ""
    method = ['GET']
    rule = "/index/update"

