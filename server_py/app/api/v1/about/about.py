#!/usr/bin/env python3

from lime.exceptions import abort
from lime.context import AppRequestContext
from app.model import Article
from app.consts import RespCode
from app.api.decorators import api_cache
from app.api.desc import ApiDescBase, api_desc_wrapper
from app.api._utils import md2html
from .. import api_group


@api_group.route('/about')
@api_cache()
def about(ctx: AppRequestContext):
    """网站相关"""
    article = Article.find_by_title('about')
    if not article:
        abort(RespCode.error, "about not found")

    article = Article.get_with_more_detail(article.id)

    # ct: article content type
    toc = None
    ct = ctx.request.query('ct')
    if ct == 'html' and article.content:
        article.content, toc = md2html(article.content)

    resp = {
        "article": article,
        "toc": toc,
    }

    return resp


@api_group.route('/about/desc', methods=('GET', ))
@api_desc_wrapper()
class ApiAboutDesc(ApiDescBase):
    name = "网站相关"
    desc = ""
    method = ['GET']
    rule = "/api/about"

    def req_args(self):
        args = [
            # (key, name, type, default, required, desc)
            # (字段，字段名称，字段类型，默认值，是否必传，备注描述)
            ('ct', '内容类型', 'string', '', 0, 'ct=html, 文章内容会由markdown转换为html返回'),
        ]
        return args

    @property
    def example(self):
        r = {
            "url": self.url + '?ct=html',
            "request": {},
            "response": {
                "code": 0,
                "data": {
                    "article": {
                        "id": 5,
                        "created_at": "2019-12-20 23:47:51",
                        "updated_at": "2019-12-27 23:18:35",
                        "user_id": 1,
                        "cate_id": 1,
                        "title": "about",
                        "content": "<h1 id=\"hello\">hello</h1>\n<p>world</p>",
                        "status": 2,
                        "user": {
                            "id": 1,
                            "created_at": "2019-12-20 23:38:53",
                            "updated_at": "2019-12-20 23:38:53",
                            "name": "admin",
                            "role_id": 1,
                            "status": 1
                        },
                        "category": {
                            "id": 1,
                            "created_at": "2019-12-20 23:46:07",
                            "updated_at": "2019-12-20 23:46:07",
                            "name": "aaa",
                            "status": 1
                        }
                    },
                    "toc": "<div class=\"toc\">\n<ul>\n<li><a href=\"#hello\">hello</a></li>\n</ul>\n</div>\n"
                },
                "msg": "OK"
            }
        }
        return r
