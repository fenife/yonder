#!/usr/bin/env python3

from sim.context import AppRequestContext
from ses.api import api_group
from ses.desc import ApiDescBase, api_desc_wrapper


@api_group.route('/query', methods=('GET',))
def query(ctx: AppRequestContext):
    pass


@api_group.route('/query/desc', methods=('GET', ))
@api_desc_wrapper()
class SearchApiDesc(ApiDescBase):
    name = "搜索"
    desc = ""
    method = ['GET']
    rule = "/search/query"

