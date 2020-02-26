#!/usr/bin/env python3

from sim.exceptions import abort
from sim.context import AppRequestContext
from wes.model import Category
from wes.consts import RespCode
from wes.api.decorators import api_cache
from wes.api.desc import ApiDescBase, api_desc_wrapper
from .. import api_group
from ._internal import get_cid_from_request


@api_group.route('/category/detail', methods=('GET', ))
@api_cache()
def category_detail(ctx: AppRequestContext):
    cid = get_cid_from_request(ctx)

    cate = Category.find(cid)
    if not cate:
        abort(RespCode.error, "category not found")

    return cate


@api_group.route('/category/detail/desc', methods=('GET', ))
@api_desc_wrapper()
class ApiCateDetailDesc(ApiDescBase):
    name = "分类详情"
    desc = ""
    method = ['GET']
    rule = "/api/category/detail"

    def req_args(self):
        args = [
            # (key, name, type, default, required, desc)
            # (字段，字段名称，字段类型，默认值，是否必传，备注描述)
            ('cid', '分类ID', 'number', '', 1, ''),
        ]
        return args

    @property
    def example(self):
        r = {
            "url": self.url + "?cid=3",
            "request": {},
            "response": {
                "code": 0,
                "data": {
                    "id": 3,
                    "created_at": "2019-12-22 22:18:18",
                    "updated_at": "2020-01-12 11:15:58",
                    "name": "afdsfde",
                    "status": 1
                },
                "msg": "OK"
            }
        }

        return r
