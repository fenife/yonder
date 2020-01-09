#!/usr/bin/env python3

import hashlib
from sim.exceptions import abort
from sim.response import Response
from sim.context import AppRequestContext
from .. import app, db, cache_pool
from ..model import User, Category, Article
from ..consts import RespCode, Permission, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from ..decorators import api_cache
from ._utils import md2html


@app.route('/api/about')
@api_cache()
def about(ctx: AppRequestContext):
    article = Article.find_by_title('about')
    if not article:
        abort(RespCode.error, "about not found")

    article = Article.get_with_more_detail(article.id)

    # ct: article content type
    ct = ctx.request.query('ct')
    if ct == 'html' and article.content:
        article.content = md2html(article.content)

    return article
