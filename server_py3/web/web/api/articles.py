#!/usr/bin/env python3

import hashlib
from sim.exceptions import abort
from sim.response import Response
from sim.context import AppRequestContext
from .. import app, db, cache_pool
from ..model import User, Category, Article
from ..consts import RespCode, Permission, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from ..decorators import permission_required, login_required, api_cache
from ._internal import to_int, get_page_from_request, get_limit_from_request, clear_cache_data


def content_hash(content):
    """计算文章内容的hash，用于对比更新前后内容是否有改变"""
    if not content:
        return

    m = hashlib.md5()
    m.update(content.encode('utf-8'))
    h = m.hexdigest()
    return h


def get_aid_from_request(ctx):
    # aid: article id
    aid = ctx.request.get_param('aid')
    aid = to_int('aid', aid)

    return aid


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

    article.user = user.without_password()
    article.category = cate

    # 创建新文章后，清除文章列表等缓存，以展示最新的文章
    clear_cache_data('/api/article*')
    clear_cache_data('/api/archive*')

    return article


@app.route('/api/article/:aid', methods=('PUT', ))
@permission_required(Permission.admin)
def article_update(ctx):
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

    """
    # get user
    user = ctx.user
    assert isinstance(user, User)
    article.user = user.without_password()

    cate = Category.find(article.id)
    article.category = cate
    """

    update_fields = []
    if 'cate_id' in input_json:
        cate_id = to_int('cate_id', input_json.pop('cate_id'))

        # category id need update
        if cate_id != article.cate_id:
            cate = Category.find(cate_id)
            if cate is None:
                abort(RespCode.error, f"category not existed")

            article.cate_id = cate_id
            article.category = cate
            update_fields.append('cate_id')

    if 'title' in input_json:
        new_title = input_json.pop('title')

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
        new_content = input_json.pop('content')

        # content need update
        if content_hash(new_content) != content_hash(article.content):
            article.content = new_content
            update_fields.append('content')

    if 'status' in input_json:
        new_status = to_int('status', input_json.pop('status'))
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


@app.route('/api/article', methods=('GET', ))
@api_cache()
def article_list(ctx: AppRequestContext):
    # 参数处理
    cate_id = ctx.request.query('cate_id')
    if cate_id is not None:
        cate_id = to_int('cate_id', cate_id)

    page = get_page_from_request(ctx)
    limit = get_limit_from_request(ctx)

    # 可展示的文章总数
    sql_for_count = """
    select count(1) as total
    from articles a
    inner join users b on a.user_id = b.id
    inner join categories c on a.cate_id = c.id
    where a.status = ? and b.status = ? and c.status = ?
    """

    # 可展示的文章列表
    sql = """
    select 
        a.id, a.title, a.created_at, a.updated_at, 
        a.user_id, b.name as user_name,
        a.cate_id, c.name as cate_name
    from articles a
    inner join users b on a.user_id = b.id
    inner join categories c on a.cate_id = c.id
    where a.status = ? and b.status = ? and c.status = ?
    """

    args = [
        ARTICLE.status.active, USER.status.active, CATEGORY.status.active,
    ]

    # 分类
    if cate_id is not None:
        extra = " and c.id = ?"
        sql_for_count += extra
        sql += extra
        args.append(cate_id)

    # 可展示的文章总数
    # 应该先查询，后面args会变化
    res = db.select(sql_for_count, args)
    if not res:
        abort(RespCode.error, "can not get article total counts")

    total = res[0].get('total')

    # 排序
    sql += " order by a.id desc"

    # 分页
    sql += " limit ?, ?"
    args += [(page - 1) * limit, limit]

    items = db.select(sql, args)

    resp = {
        "articles": items,
        "total": total
    }

    return resp


@app.route('/api/article/:aid', methods=('GET', ))
@api_cache()
def article_detail(ctx):
    aid = ctx.request.get_param('aid')
    try:
        aid = int(aid)
    except Exception as e:
        app.logger.error(f"aid must be an integer, but get: {aid}")
        abort(RespCode.error, "in GET method, aid must be an integer")

    # aid = get_aid_from_request(ctx)

    article = Article.get_with_more_detail(aid)
    if not article:
        abort(RespCode.error, "article not found")

    _pre = article.get_pre()
    _next = article.get_next()

    resp = {
        "article": article,
        "pre": _pre,
        "next": _next,
    }

    return resp


