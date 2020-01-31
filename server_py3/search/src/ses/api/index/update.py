#!/usr/bin/env python3

from sim.exceptions import abort
from sim.context import AppRequestContext
from ses.api import api_group
from ses.desc import ApiDescBase, api_desc_wrapper
from ses.consts import RespCode
from ses.engine.build import build


@api_group.route('/index/update', methods=('POST',))
def update(ctx: AppRequestContext):
    input_json = ctx.request.json()
    if not input_json:
        abort(RespCode.error, "body is empty")

    required = ('id', 'title')
    for field in required:
        if field not in input_json:
            abort(RespCode.error, f"field `{field}` is required")

    try:
        build(input_json)
    except Exception as e:
        abort(RespCode.error, str(e))


@api_group.route('/index/update/desc', methods=('POST', ))
@api_desc_wrapper()
class SearchApiDesc(ApiDescBase):
    name = "建索引"
    desc = ""
    method = ['POST']
    rule = "/search/index/update"

    def req_body(self):
        # {
        #     "id": 2,
        #     "title": "aaaa",
        #     "created_at": "2019-12-20 23:47:37",
        #     "updated_at": "2020-01-12 15:55:58",
        #     "user_id": 1,
        #     "user_name": "admin",
        #     "cate_id": 1,
        #     "cate_name": "aaa"
        # }
        body = [
            # (key, name, type, default, required, desc)
            ('id',      '文章ID',  'number', '', 1, ''),
            ('title',   '文章标题', 'string', '', 1, ''),
        ]
        return body

    @property
    def example(self):
        r = {
            "url": self.url,
            "request": {
                "body": {
                    "title": "aafdsfds",
                    "id": 2
                }
            },
            "response": {
                "code": 0,
                "data": {},
                "msg": "OK"
            }
        }
        return r
