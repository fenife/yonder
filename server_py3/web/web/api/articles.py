#!/usr/bin/env python3

from sim.exceptions import abort
from .. import app, db, cache_pool
from ..model import User, Category, Article
from ..consts import RespCode, Permission, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from ..decorators import permission_required, login_required


@app.route('/api/article', methods=('POST', ))
@permission_required(Permission.admin)
def article_create(ctx):
    """
    input:
    {
        "title": "aaa",
        "content": "abc",
        "cate_id": 1
    }
    """
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

    # get user_id
    user = ctx.user
    assert isinstance(user, User)

    # if category existed
    cate_id = input_json['cate_id']
    try:
        cate_id = int(cate_id)
    except Exception as e:
        abort(RespCode.error, f"cate_id must be an interger, but get: `{cate_id}`")

    # check if category name existed
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

    return article
