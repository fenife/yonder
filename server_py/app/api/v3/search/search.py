#!/usr/bin/env python3

import requests
from lime.exceptions import abort
from lime.response import Response
from lime.context import AppRequestContext
from app import app, db, cache_pool
from app.model import User, Category, Article
from app.consts import RespCode, Permission, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from app.api.decorators import permission_required, login_required
from app.api.desc import ApiDescBase, api_desc_wrapper
from app.api._utils import call_go_search
from .. import api_group_v3


@api_group_v3.route('/search')
def search(ctx: AppRequestContext):
    """搜索"""
    # 参数处理
    kw = ctx.request.get_uri_arg('kw')
    if not kw:
        abort(RespCode.error, "params `kw` is required")

    page = ctx.request.get_uri_arg('page')
    limit = ctx.request.get_uri_arg('limit')

    res = call_go_search(kw, page, limit)
    resp = Response(data=res['data'], code=res['code'], msg=res['msg'])
    return resp


@api_group_v3.route('/search/desc', methods=('GET', ))
@api_desc_wrapper()
class ApiSearchDesc(ApiDescBase):
    name = "搜索"
    desc = ""
    method = ['GET']
    rule = "/api/search"

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
