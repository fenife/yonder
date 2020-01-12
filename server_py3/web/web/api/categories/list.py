#!/usr/bin/env python3

from sim.exceptions import abort
from sim.context import AppRequestContext
from ...model import Category
from ...consts import RespCode, Permission, CATEGORY
from ...decorators import permission_required, api_cache
from ...desc import ApiDescBase, api_desc_wrapper
from ... import app, db
from .. import api_group
from .._utils import clear_cache_data, to_int


@api_group.route('/category/list', methods=('GET', ))
@api_cache()
def category_list(ctx: AppRequestContext):
    # 暂时返回全部分类（包括status为delete的分类）
    data = Category.find_all()

    sql = """
    select cate_id, count(1) as cnt from articles where status = 1 group by cate_id
    """
    res = db.select(sql)
    if not res:
        # abort(RespCode.error, "can not count articles")
        app.logger.error(f"can not count articles, {sql}")

    counts = {d['cate_id']: d['cnt'] for d in res} if res else {}
    for cate in data:
        # 该分类下可展示文章的数目
        cate.article_count = counts.get(cate.id, 0)

    return data


@api_group.route('/category/list/desc', methods=('GET', ))
@api_desc_wrapper()
class ApiArticleListDesc(ApiDescBase):
    name = "分类列表"
    desc = ""
    method = ['GET']
    rule = "/api/category/list"

    @property
    def example(self):
        r = {
            "url": self.url,
            "request": {},
            "response": {
                "code": 0,
                "data": [
                    {
                        "id": 1,
                        "created_at": "2019-12-15 14:16:10",
                        "updated_at": "2020-01-12 11:14:58",
                        "name": "ccccde",
                        "status": 1,
                        "article_count": 8
                    }
                ],
                "msg": "OK"
            }
        }
        return r
