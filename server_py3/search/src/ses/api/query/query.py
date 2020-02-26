#!/usr/bin/env python3

from sim.exceptions import abort
from sim.context import AppRequestContext
from ses.api import api_group
from ses.api.desc import ApiDescBase, api_desc_wrapper
from ses.consts import RespCode
from ses.engine.query import search
from ses.api._utils import get_page_from_request, get_limit_from_request


@api_group.route('/query', methods=('GET',))
def query(ctx: AppRequestContext):
    kw = ctx.request.get_uri_arg('kw')
    if not kw:
        abort(RespCode.error, "params `kw` is required")

    page = get_page_from_request(ctx)
    limit = get_limit_from_request(ctx)

    articles = []
    total = 0

    items = search(kw)
    if items:
        # 分页
        articles = items[(page - 1) * limit: page * limit]
        total = len(items)

    resp = {
        "articles": articles,
        "total": total,
    }
    return resp


@api_group.route('/query/desc', methods=('GET', ))
@api_desc_wrapper()
class SearchApiDesc(ApiDescBase):
    name = "搜索"
    desc = ""
    method = ['GET']
    rule = "/search/query"

    def req_args(self):
        args = [
            # (key, name, type, default, required, desc)
            # (字段，字段名称，字段类型，默认值，是否必传，备注描述)
            ('kw',      '搜索的关键字',   'string', '', 1, ''),
            ('page',    '页码',         'number', 1,  0, '第几页，从1开始'),
            ('limit',   '每页的限制条目', 'number', 10, 0, '配置中可指定该值'),
        ]
        return args

    @property
    def example(self):
        r = {
            "url": self.url + '?kw=aaa&page=1&limit=2',
            "request": {},
            "response": {
                "code": 0,
                "data": {
                    "articles": [
                        {
                            "id": 2,
                            "title": "aaaa",
                            "created_at": "2019-12-20 23:47:37",
                            "updated_at": "2020-01-12 15:55:58",
                            "user_id": 1,
                            "user_name": "admin",
                            "cate_id": 1,
                            "cate_name": "aaa"
                        }
                    ],
                    "total": 1
                },
                "msg": "OK"
            }
        }
        return r
