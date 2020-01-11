#!/usr/bin/env python3

from sim.exceptions import abort
from sim.context import AppRequestContext

from ...model import User, Category, Article
from ...consts import RespCode, Permission, ARTICLE
from ...decorators import permission_required, api_cache
from ...desc import ApiDescBase, api_desc_wrapper
from .. import app, api_group
from .._utils import md2html
from ._internal import get_aid_from_request


@app.route('/api/article/:aid', methods=('GET', ))
@api_group.route('/article/detail', methods=('GET', ))
@api_cache()
def article_detail(ctx: AppRequestContext):
    aid = get_aid_from_request(ctx)

    article = Article.get_with_more_detail(aid)
    if not article:
        abort(RespCode.error, "article not found")

    # ct: article content type
    ct = ctx.request.query('ct')
    if ct == 'html' and article.content:
        article.content = md2html(article.content)

    _pre = article.get_pre()
    if _pre:
        # 暂时不需要展示content内容，减少带宽占用
        _pre.pop('content', None)

    _next = article.get_next()
    if _next:
        # 暂时不需要展示content内容，减少带宽占用
        _next.pop('content', None)

    resp = {
        "article": article,
        "pre": _pre,
        "next": _next,
    }

    return resp


@api_group.route('/article/detail/desc', methods=('GET', ))
# @permission_required(Permission.admin)
@api_desc_wrapper()
class ApiArticleCreateDesc(ApiDescBase):
    name = "文章详情"
    desc = ""
    method = ['GET']
    rule = "/api/article/detail"

    def req_args(self):
        args = [
            # (key, name, type, default, required, desc)
            # (字段，字段名称，字段类型，默认值，是否必传，备注描述)
            ('aid', '文章ID', 'number', '', 1, ''),
            ('ct', '内容类型', 'string', '', 0, 'ct=html, 文章内容会由markdown转换为html返回'),
        ]
        return args

    @property
    def example(self):
        r = {
            "url": self.url + "?aid=1&ct=html",
            "request": {},
            "response": {
                "code": 0,
                "data": {
                    "article": {
                        "id": 2,
                        "created_at": "2017-12-15 17:44:31",
                        "updated_at": "2020-01-11 12:48:00",
                        "user_id": 1,
                        "cate_id": 2,
                        "title": "aafdsfds",
                        "content": "<p>afadasdf</p>",
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
                    "pre": {
                        "id": 1,
                        "created_at": "2017-12-15 17:43:19",
                        "updated_at": "2019-12-16 22:54:19",
                        "user_id": 1,
                        "cate_id": 1,
                        "title": "aaaaa",
                        "status": 1
                    },
                    "next": {
                        "id": 3,
                        "created_at": "2018-12-15 17:49:52",
                        "updated_at": "2019-12-25 21:40:33",
                        "user_id": 1,
                        "cate_id": 2,
                        "title": "aafdafds",
                        "status": 1
                    }
                },
                "msg": "OK"
            }
        }
        return r
