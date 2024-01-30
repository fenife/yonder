#!/usr/bin/env python3

import markdown
import datetime
import requests
from sim.context import AppRequestContext
from sim.exceptions import abort
from wes import app, db, cache_pool
from wes.consts import RespCode


# 每页展示的文章数目
DEFAULT_PAGE_SIZE = 10


def to_int(var_name, val) -> int:
    """
    将某个变量转换为int类型的值

    主要用于转换http请求的参数
    同时也相当于作校验，如果失败，直接抛出异常(abort)

    :param var_name: 参数名称，用于提示
    :param val: 要转换的值
    """
    if not val:
        abort(RespCode.error, f"arg `{var_name}` is required")

    try:
        val = int(val)
    except Exception as e:
        # app.logger.error(f"{var_name} must be an integer, but get: {val}")
        abort(RespCode.error, f"{var_name} must be an integer, but get: '{val}';")

    return val


def get_page_from_request(ctx: AppRequestContext) -> int:
    """
    从http请求中获取参数page，如果请求中没有该参数，则返回默认值 1

    比如请求的url为：
    /api/search?kw='aaa'&page=1&limit=2

    则返回page：
    1
    """
    page = ctx.request.query('page')
    if page is None:
        page = 1
    else:
        page = to_int('page', page)

    if page <= 0:
        abort(RespCode.error, "page must be greater than 0")

    return page


def get_limit_from_request(ctx: AppRequestContext) -> int:
    """
    从http请求中获取参数limit，如果请求中没有该参数，则返回默认值 DEFAULT_PAGE_SIZE

    比如请求的url为：
    /api/search?kw='aaa'&page=1&limit=2

    则返回limit：
    2
    """
    limit = ctx.request.query('limit')
    if limit is None:
        limit = app.config.get("PAGE_SIZE", DEFAULT_PAGE_SIZE)
    else:
        limit = to_int('limit', limit)

    if not 0 < limit <= 100:
        abort(RespCode.error, "limit must be between 0 and 100")

    return limit


def clear_cache_data(pattern: str):
    """清除缓存"""
    with cache_pool.get() as rds:
        keys = rds.keys(pattern)
        app.logger.info(f"clear keys, pat: `{pattern}`, len: {len(keys)}")
        if keys:
            rds.delete(*keys)

        # for key in rds.scan_iter(pattern):
        #     rds.delete(key)


def md2html(content):
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.tables',
        'markdown.extensions.toc',
    ])
    html = md.convert(content)
    toc = md.toc        # top of content

    # print(md.toc_tokens)      # 非html的toc

    if toc == """<div class="toc">\n<ul></ul>\n</div>\n""":
        # 相当于目录为空
        toc = None

    return html, toc


def build_search_index(aid):
    """
    更新索引
    :param aid: article id
    :return:
    """

    sql = f"""
    select 
        a.id, a.title, a.created_at, a.updated_at, 
        a.user_id, b.name as user_name,
        a.cate_id, c.name as cate_name
    from articles a
    inner join users b on a.user_id = b.id
    inner join categories c on a.cate_id = c.id
    where a.id = {aid}"""
    items = db.select(sql)
    if not items:
        raise Exception(f"can not get article, id: {aid}")

    r = call_ses_update(items[0])
    return r


def call_ses_update(article):
    """
    调用搜索服务的接口更新索引
    :param article:
    {
        "title": "test",
        "id": 2
    }
    """
    # http://127.0.0.1:6090/search/query?kw=py&page=1&limit=2
    url = "http://127.0.0.1:6090/search/index/update"
    headers = {
        "Content-Type": "application/json",
    }

    # 解决requests报错：Object of type 'datetime' is not JSON serializable
    for k, v in article.items():
        if isinstance(v, datetime.datetime):
            article[k] = str(v)

    app.logger.debug(article)
    resp = requests.post(url, json=article, headers=headers, timeout=60)
    res = resp.json()
    return res


def call_ses_query(kw, page, limit):
    """调用搜索服务的接口获取搜索结果"""
    # http://127.0.0.1:6090/search/query?kw=py&page=1&limit=2
    url = "http://127.0.0.1:6090/search/query"
    url += f"?kw={kw}"
    if page:
        url += f"&page={page}"

    if limit:
        url += f"&limit={limit}"

    resp = requests.get(url)
    res = resp.json()
    return res


def call_go_search(kw, page, limit):
    """调用搜索服务的接口获取搜索结果"""
    # http://127.0.0.1:6090/search/query?kw=py&page=1&limit=2
    url = "http://127.0.0.1:6060/api/search"
    url += f"?kw={kw}"
    if page:
        url += f"&page={page}"

    if limit:
        url += f"&limit={limit}"

    resp = requests.get(url)
    res = resp.json()
    return res
