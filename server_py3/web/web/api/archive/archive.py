#!/usr/bin/env python3

from sim.exceptions import abort
from sim.response import Response
from sim.context import AppRequestContext
from ... import app, db, cache_pool
from ...model import User, Category, Article
from ...consts import RespCode, Permission, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from ...decorators import api_cache
from ...desc import ApiDescBase, api_desc_wrapper
from .. import api_group


@api_group.route('/archive')
@api_cache()
def archive(ctx: AppRequestContext):
    """归档"""
    sql = """
    select 
        a.id, a.title, a.created_at, a.updated_at, 
        a.user_id, b.name as user_name,
        a.cate_id, c.name as cate_name
    from articles a
    inner join users b on a.user_id = b.id
    inner join categories c on a.cate_id = c.id
    where a.status = ? and b.status = ? and c.status = ?
    order by a.id desc
    """

    args = [
        ARTICLE.status.active, USER.status.active, CATEGORY.status.active,
    ]

    items = db.select(sql, args)
    if not items:
        abort(RespCode.error, "can not get article list")

    # 默认按id倒序排序，亦即创建时间(create_at)
    year_dict = {}
    for art in items:
        # assert isinstance(art, Article)
        year = art["created_at"].year
        if year not in year_dict:
            year_dict[year] = {
                "year": year,
                "art_list": [],
                "count": 0,
            }

        year_dict[year]["art_list"].append(art)
        year_dict[year]["count"] += 1

    resp = list(year_dict.values())

    return resp


@api_group.route('/archive/desc', methods=('GET', ))
@api_desc_wrapper()
class ApiArchiveDesc(ApiDescBase):
    name = "归档"
    desc = ""
    method = ['GET']
    rule = "/api/archive"

    @property
    def example(self):
        r = {
            "url": self.url,
            "request": {},
            "response": {
                "code": 0,
                "data": [
                    {
                        "year": 2020,
                        "art_list": [
                            {
                                "id": 13,
                                "title": "sfsdfds",
                                "created_at": "2020-01-12 15:57:13",
                                "updated_at": "2020-01-12 15:57:13",
                                "user_id": 1,
                                "user_name": "admin",
                                "cate_id": 1,
                                "cate_name": "aaa"
                            },
                            {
                                "id": 12,
                                "title": "fdsfsd",
                                "created_at": "2020-01-12 15:57:02",
                                "updated_at": "2020-01-12 15:57:02",
                                "user_id": 1,
                                "user_name": "admin",
                                "cate_id": 2,
                                "cate_name": "bbb"
                            }
                        ],
                        "count": 2
                    },
                    {
                        "year": 2019,
                        "art_list": [
                            {
                                "id": 11,
                                "title": "jfdksfd",
                                "created_at": "2019-12-26 23:15:09",
                                "updated_at": "2019-12-26 23:15:09",
                                "user_id": 1,
                                "user_name": "admin",
                                "cate_id": 2,
                                "cate_name": "bbb"
                            },
                        ],
                        "count": 1
                    }
                ],
                "msg": "OK"
            }
        }
        return r
