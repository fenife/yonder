#!/usr/bin/env python3

from sim.exceptions import abort
from sim.response import Response
from sim.context import AppRequestContext

from web import app, db, cache_pool
from web.model import User, Category, Article
from web.consts import RespCode, Permission, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from web.decorators import permission_required, login_required, api_cache
from web.api._utils import (
    to_int, get_page_from_request, get_limit_from_request, clear_cache_data, md2html
)
from ...desc import ApiDescBase, api_desc_wrapper
from .. import api_group


@app.route('/api/article/list', methods=('GET', ))
@api_cache()
def article_list(ctx: AppRequestContext):
    # 参数处理
    cate_id = ctx.request.query('cate_id')
    if cate_id is not None:
        cate_id = to_int('cate_id', cate_id)

    page = get_page_from_request(ctx)
    limit = get_limit_from_request(ctx)

    # 可展示的文章总数
    sql_for_count = """
    select count(1) as total
    from articles a
    inner join users b on a.user_id = b.id
    inner join categories c on a.cate_id = c.id
    where a.status = ? and b.status = ? and c.status = ?
    """

    # 可展示的文章列表
    sql = """
    select 
        a.id, a.title, a.created_at, a.updated_at, 
        a.user_id, b.name as user_name,
        a.cate_id, c.name as cate_name
    from articles a
    inner join users b on a.user_id = b.id
    inner join categories c on a.cate_id = c.id
    where a.status = ? and b.status = ? and c.status = ?
    """

    args = [
        ARTICLE.status.active, USER.status.active, CATEGORY.status.active,
    ]

    # 分类
    if cate_id is not None:
        extra = " and c.id = ?"
        sql_for_count += extra
        sql += extra
        args.append(cate_id)

    # 可展示的文章总数
    # 应该先查询，后面args会变化
    res = db.select(sql_for_count, args)
    if not res:
        abort(RespCode.error, "can not get article total counts")

    total = res[0].get('total')

    # 排序
    sql += " order by a.id desc"

    # 分页
    sql += " limit ?, ?"
    args += [(page - 1) * limit, limit]

    items = db.select(sql, args)

    resp = {
        "articles": items,
        "total": total
    }

    return resp


@api_group.route('/article/list/desc', methods=('GET', ))
# @permission_required(Permission.admin)
@api_desc_wrapper()
class ApiArticleCreateDesc(ApiDescBase):
    name = "文章列表"
    desc = ""
    method = ['GET']
    rule = "/api/article/list"

    def req_args(self):
        args = [
            # (key, name, type, default, required, desc)
            # (字段，字段名称，字段类型，默认值，是否必传，备注描述)
            ('cate_id', '分类ID',       'number', '', 0, ''),
            ('page',    '页码',         'number', 1,  0, '第几页，从1开始'),
            ('limit',   '每页的限制条目', 'number', 10, 0, '配置中可指定该值'),
        ]
        return args

    @property
    def example(self):
        r = {
            "url": self.url + "?cate_id=2&page=2&limit=2",
            "request": {},
            "response": {
                "code": 0,
                "data": {
                    "articles": [
                        {
                            "id": 21,
                            "title": "aafdafdas",
                            "created_at": "2020-01-11 10:31:21",
                            "updated_at": "2020-01-11 10:31:21",
                            "user_id": 1,
                            "user_name": "admin",
                            "cate_id": 2,
                            "cate_name": "aaaa"
                        },
                        {
                            "id": 20,
                            "title": "aafdfds",
                            "created_at": "2019-12-25 21:37:51",
                            "updated_at": "2019-12-25 22:50:05",
                            "user_id": 1,
                            "user_name": "admin",
                            "cate_id": 2,
                            "cate_name": "aaaa"
                        }
                    ],
                    "total": 12
                },
                "msg": "OK"
            }
        }
        return r
