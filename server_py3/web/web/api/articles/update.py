#!/usr/bin/env python3

from sim.exceptions import abort
from sim.context import AppRequestContext
from sim.response import Response

from ...model import User, Category, Article
from ...consts import RespCode, Permission, ARTICLE
from ...decorators import permission_required
from ...desc import ApiDescBase, api_desc_wrapper
from .. import app, api_group
from .._utils import to_int, clear_cache_data
from ._internal import content_hash, get_aid_from_request


# 可添加多个路由，兼容旧的api
@app.route('/api/article/:aid', methods=('PUT', ))
@api_group.route('/article/update', methods=('PUT', ))
@permission_required(Permission.admin)
def article_update(ctx: AppRequestContext):
    aid = get_aid_from_request(ctx)

    input_json = ctx.request.json()
    if not input_json:
        abort(RespCode.error, "body is empty")

    supported = {'cate_id', 'title', 'content', 'status'}
    unsupported = set(input_json.keys()) - supported
    if unsupported:
        abort(RespCode.error, f"unsupported fields: {list(unsupported)}")

    article = Article.get_with_more_detail(aid)
    if not article:
        abort(RespCode.error, "article not found")

    update_fields = []
    if 'cate_id' in input_json:
        cate_id = to_int('cate_id', input_json.get('cate_id'))

        # category id need update
        if cate_id != article.cate_id:
            cate = Category.find(cate_id)
            if cate is None:
                abort(RespCode.error, f"category not existed")

            article.cate_id = cate_id
            article.category = cate
            update_fields.append('cate_id')

    if 'title' in input_json:
        new_title = input_json.get('title')

        # title need update
        if new_title != article.title:
            # prevent xss of title
            new_title = Article.valid_title(new_title)

            # if new title existed
            art = Article.find_by_title(new_title)
            if art:
                abort(RespCode.error, f"title existed")

            article.title = new_title
            update_fields.append('title')

    if 'content' in input_json:
        new_content = input_json.get('content')

        # content need update
        if content_hash(new_content) != content_hash(article.content):
            article.content = new_content
            update_fields.append('content')

    if 'status' in input_json:
        new_status = to_int('status', input_json.get('status'))
        if new_status != article.status:
            article.status = new_status
            update_fields.append('content')

    if update_fields:
        app.logger.info(f"update fields: {update_fields}")
        if article.modify() is False:
            abort(RespCode.error, "update article error")

        # 更新成功后，清除该文章详情的缓存
        clear_cache_data(f"/api/article/{article.id}*")

        return article

    else:
        return Response(
            data=article,
            code=200,
            msg="article is the same as before, no need to update"
        )


@api_group.route('/article/update/desc', methods=('PUT', ))
@permission_required(Permission.admin)
@api_desc_wrapper()
class ApiArticleCreateDesc(ApiDescBase):
    name = "文章更新"
    desc = ""
    method = ['PUT']
    rule = "/api/article/update"

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
