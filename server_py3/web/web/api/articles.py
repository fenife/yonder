#!/usr/bin/env python3

import hashlib
from sim.exceptions import abort
from sim.response import Response
from .. import app, db, cache_pool
from ..model import User, Category, Article
from ..consts import RespCode, Permission, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from ..decorators import permission_required, login_required


def content_hash(content):
    """计算文章内容的hash，用于对比更新前后内容是否有改变"""
    if not content:
        return

    m = hashlib.md5()
    m.update(content.encode('utf-8'))
    h = m.hexdigest()
    return h


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

    # get user
    user = ctx.user
    assert isinstance(user, User)

    # if category existed
    cate_id = input_json['cate_id']
    try:
        cate_id = int(cate_id)
    except Exception as e:
        abort(RespCode.error, f"cate_id must be an integer, but get: `{cate_id}`")

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

    return article


@app.route('/api/article/:aid', methods=('PUT', ))
@permission_required(Permission.admin)
def article_update(ctx):
    aid = ctx.request.get_param('aid')
    try:
        aid = int(aid)
    except Exception as e:
        app.logger.error(f"aid must be an integer, but get: {aid}")
        abort(RespCode.error, "aid must be an integer")

    input_json = ctx.request.json()
    if not input_json:
        abort(RespCode.error, "body is empty")

    supported = {'cate_id', 'title', 'content'}
    unsupported = set(input_json.keys()) - supported
    if unsupported:
        abort(RespCode.error, f"unsupported fields: {list(unsupported)}")

    article = Article.find(aid)
    if not article:
        abort(RespCode.error, "article not found")

    # get user
    user = ctx.user
    assert isinstance(user, User)

    cate = Category.find(article.id)
    article.category = cate

    need_update = False
    if 'cate_id' in input_json:
        cate_id = input_json.pop('cate_id')

        # categroy id need update
        if cate_id != article.cate_id:
            cate = Category.find(cate_id)
            if cate is None:
                abort(RespCode.error, f"category not existed")

            article.cate_id = cate_id
            article.category = cate
            need_update = True

    if 'title' in input_json:
        new_title = input_json.pop('title')

        # title need update
        if new_title != article.title:
            # prevent xss of title
            new_title = Article.valid_title(new_title)

            # if new title existed
            old = Article.find_by_title(new_title)
            if old:
                abort(RespCode.error, f"title existed")

            article.title = new_title
            need_update = True

    if 'content' in input_json:
        new_content = input_json.pop('content')

        # content need update
        if content_hash(new_content) != content_hash(article.content):
            article.content = new_content
            need_update = True

    article.user = user.without_password()

    if need_update:
        if article.modify() is False:
            abort(RespCode.error, "update article error")

        return article

    else:
        return Response(
            data=article,
            code=200,
            msg="article is the same as before, no need to update"
        )


@app.route('/api/article', methods=('GET', ))
def article_list(ctx):
    return


@app.route('/api/article/:aid', methods=('GET', ))
def article_detail(ctx):
    aid = ctx.request.get_param('aid')
    try:
        aid = int(aid)
    except Exception as e:
        app.logger.error(f"aid must be an integer, but get: {aid}")
        abort(RespCode.error, "in GET method, aid must be an integer")

    article = Article.find(aid)
    if not article:
        abort(RespCode.error, "article not found")

    return article
