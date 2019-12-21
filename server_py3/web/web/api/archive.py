#!/usr/bin/env python3

from sim.exceptions import abort
from sim.response import Response
from sim.context import AppRequestContext
from .. import app, db, cache_pool
from ..model import User, Category, Article
from ..consts import RespCode, Permission, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from ..decorators import permission_required, login_required


@app.route('/api/archive')
def archive(ctx: AppRequestContext):
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
    # print(resp)

    return resp
