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

    def req_headers(self):
        headers = [
            # (key, val, desc)
            ('Cookie', 'token=xxx', "用户登录token"),
        ] + self.default_req_headers
        return headers

    def req_args(self):
        args = [
            # (key, name, type, default, required, desc)
            # (字段，字段名称，字段类型，默认值，是否必传，备注描述)
            ('aid', '文章ID', 'number', '', 1, ''),
        ]
        return args

    def req_body(self):
        # {
        # 	"title": "aafdafdas",
        # 	"content": "afadaasdf",
        # 	"cate_id": 2
        # }
        body = [
            # (key, name, type, default, required, desc)
            ('title',   '文章标题', 'string', '', 0, ''),
            ('content', '文章内容', 'string', '', 0, ''),
            ('cate_id', '分类ID',   'number', '', 0, ''),
            ('status',  '文章状态', 'number', '', 0, '枚举值: 0 不可见; 1 可见;'),
        ]
        return body

    @property
    def example(self):
        r = {
            "url": self.url + "?aid=2",
            "note": "先登录，请求头部Cookie带上token",
            "request": {
                "body": {
                    "title": "aafdsfds",
                    "content": "afadasdf",
                    "cate_id": 2
                }
            },
            "response": {
                "code": 0,
                "data": {
                    "id": 2,
                    "created_at": "2017-12-15 17:44:31",
                    "updated_at": "2020-01-11 12:48:00",
                    "user_id": 1,
                    "cate_id": 2,
                    "title": "aafdsfds",
                    "content": "afadasdf",
                    "status": 1,
                    "user": {
                        "id": 1,
                        "created_at": "2019-12-28 15:11:02",
                        "updated_at": "2019-12-28 15:11:02",
                        "name": "admin",
                        "role_id": 1,
                        "status": 1
                    },
                    "category": {
                        "id": 2,
                        "created_at": "2019-12-15 16:04:20",
                        "updated_at": "2019-12-15 16:04:20",
                        "name": "aaaa",
                        "status": 1
                    }
                },
                "msg": "OK"
            }
        }
        return r
