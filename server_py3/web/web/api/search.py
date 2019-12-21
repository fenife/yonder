#!/usr/bin/env python3

import hashlib
from sim.exceptions import abort
from sim.response import Response
from sim.context import AppRequestContext
from .. import app, db, cache_pool
from ..model import User, Category, Article
from ..consts import RespCode, Permission, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from ..decorators import permission_required, login_required
from ._internal import get_page_from_request, get_limit_from_request


@app.route('/api/search')
def search(ctx: AppRequestContext):
    # 参数处理
    kw = ctx.request.query('kw')
    if not kw:
        abort("params `kw` is required")

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
    """

    args = [
        ARTICLE.status.active, USER.status.active, CATEGORY.status.active,
        f"%{kw}%"
    ]

    # 分页
    sql += " limit ?, ?"
    args += [(page - 1) * limit, limit]

    items = db.select(sql, args)

    resp = {
        "articles": items,
    }

    return resp
