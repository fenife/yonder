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
        # 	"title": "aafdafdas",
        # 	"content": "afadaasdf",
        # 	"id": 2
        # }
        body = [
            # (key, name, type, default, required, desc)
            ('title',   '文章标题', 'string', '', 0, ''),
            ('content', '文章内容', 'string', '', 0, ''),
            ('id',      '文章ID',   'number', '', 0, ''),
        ]
        return body

    @property
    def example(self):
        r = {
            "url": self.url,
            "request": {
                "body": {
                    "title": "aafdsfds",
                    "content": "afadasdf",
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
