#!/usr/bin/env python3

from sim.context import AppRequestContext
from sim.exceptions import abort
from .. import app, cache_pool
from ..consts import RespCode


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
    try:
        val = int(val)
    except Exception as e:
        app.logger.error(f"{var_name} must be an integer, but get: {val}")
        abort(RespCode.error, f"{var_name} must be an integer")

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
    with cache_pool.get() as rds:
        keys = rds.keys(pattern)
        app.logger.debug(f"clear keys, pat: `{pattern}`, len: {len(keys)}")
        if keys:
            rds.delete(*keys)

        # for key in rds.scan_iter(pattern):
        #     rds.delete(key)
