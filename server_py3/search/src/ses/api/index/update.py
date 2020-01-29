#!/usr/bin/env python3

from sim.context import AppRequestContext
from ses.api import api_group
from ses.desc import ApiDescBase, api_desc_wrapper


@api_group.route('/index/update', methods=('POST',))
def update(ctx: AppRequestContext):
    pass


@api_group.route('/index/update/desc', methods=('POST', ))
@api_desc_wrapper()
class SearchApiDesc(ApiDescBase):
    name = "建索引"
    desc = ""
    method = ['POST']
    rule = "/search/index/update"

