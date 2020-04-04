#!/usr/bin/env python3

from sim.exceptions import abort
from sim.context import AppRequestContext
from wes import db
from wes.consts import USER, CATEGORY, ARTICLE, RespCode
from wes.api.desc import ApiDescBase, api_desc_wrapper
from wes.api._utils import get_page_from_request, get_limit_from_request
from .. import api_group


@api_group.route('/search')
def search(ctx: AppRequestContext):
    """搜索"""
    # 参数处理
    kw = ctx.request.get_uri_arg('kw')
    if not kw:
        abort(RespCode.error, "params `kw` is required")

    page = get_page_from_request(ctx)
    limit = get_limit_from_request(ctx)

    sql = """
    select 
        a.id, a.title, a.created_at, a.updated_at, 
        a.user_id, b.name as user_name,
        a.cate_id, c.name as cate_name
    from articles a
    inner join users b on a.user_id = b.id
    inner join categories c on a.cate_id = c.id
    where a.status = ? and b.status = ? and c.status = ? 
    and a.title like ?
    order by a.id desc
    """

    args = [
        ARTICLE.status.active, USER.status.active, CATEGORY.status.active,
        f"%{kw}%"
    ]

    articles = []
    total = 0

    items = db.select(sql, args)
    if items:
        # 分页
        articles = items[(page-1) * limit: page * limit]
        total = len(items)

    resp = {
        "articles": articles,
        "total": total,
    }

    return resp


@api_group.route('/search/desc', methods=('GET', ))
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
