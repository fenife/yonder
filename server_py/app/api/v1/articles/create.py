#!/usr/bin/env python3

from lime.exceptions import abort
from lime.context import AppRequestContext
from app.model import User, Category, Article
from app.consts import RespCode, Permission, ARTICLE
from app.api.decorators import permission_required
from app.api.desc import ApiDescBase, api_desc_wrapper
from .. import api_group
from app.api._utils import clear_cache_data, to_int, build_search_index


@api_group.route('/article/create', methods=('POST', ))
@permission_required(Permission.admin)
def article_create(ctx: AppRequestContext):
    """文章新建"""
    input_json = ctx.request.json()
    if not input_json:
        abort(RespCode.error, "body is empty")

    required = ('cate_id', 'title', 'content')
    for field in required:
        if field not in input_json:
            abort(RespCode.error, f"field `{field}` is required")

    unsupported = set(input_json.keys()) - set(required)
    if unsupported:
        abort(RespCode.error, f"unsupported fields: {list(unsupported)}")

    # get user
    user = ctx.user
    assert isinstance(user, User)

    # if category existed
    cate_id = input_json['cate_id']
    cate_id = to_int('cate_id', cate_id)

    # check if category existed
    cate = Category.find(cate_id)
    if not cate:
        abort(RespCode.error, f"category not existed")

    # prevent xss of title
    title = Article.valid_title(input_json['title'])

    # if title existed
    old = Article.find_by_title(title)
    if old:
        abort(RespCode.error, f"title existed")

    article = Article()
    article.user_id = user.id
    article.cate_id = cate.id
    article.title = title
    article.content = input_json.get('content', None)
    article.status = ARTICLE.status.active

    article.save()
    if getattr(article, 'id', None) is None:
        abort(RespCode.error, "create new article error")

    article.user = user.without_password()
    article.category = cate

    # 创建新文章后，清除文章列表等缓存，以展示最新的文章
    clear_cache_data('/api/article*')
    clear_cache_data('/api/archive*')

    # 创建搜索服务的索引
    # build_search_index(article.id)

    return article


@api_group.route('/article/create/desc', methods=('POST', ))
@permission_required(Permission.admin)
@api_desc_wrapper()
class ApiArticleCreateDesc(ApiDescBase):
    name = "文章新建"
    desc = ""
    method = ['POST']
    rule = "/api/article/create"

    def req_headers(self):
        headers = [
            # (key, val, desc)
            ('Cookie', 'token=xxx', "用户登录token"),
        ] + self.default_req_headers
        return headers

    def req_body(self):
        # {
        # 	"title": "aafdafdas",
        # 	"content": "afadaasdf",
        # 	"cate_id": 2
        # }
        body = [
            # (key, name, type, default, required, desc)
            ('title',   '文章标题', 'string', '', 1, ''),
            ('content', '文章内容', 'string', '', 1, ''),
            ('cate_id', '分类ID',   'number', '', 1, ''),
        ]
        return body

    @property
    def example(self):
        r = {
            "url": self.url,
            "note": "先登录，请求头部Cookie带上token",
            "request": {
                "body": {
                    "title": "aaee",
                    "content": "aaee",
                    "cate_id": 2
                }
            },
            "response": {
                "code": 0,
                "data": {
                    "user_id": 1,
                    "cate_id": 2,
                    "title": "aaee",
                    "content": "aaee",
                    "status": 1,
                    "created_at": "2020-01-11 11:16:10",
                    "updated_at": "2020-01-11 11:16:10",
                    "id": 22,
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
