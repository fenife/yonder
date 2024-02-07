#!/usr/bin/env python3

from functools import wraps
from lime.exceptions import abort
from lime.context import AppRequestContext
from lime.response import Response
from app import app
from app.model import User
from app.consts import RespCode, Permission


@app.before_request
def load_user_to_context(ctx: AppRequestContext):
    """根据请求头部的Cookie获取token，再从redis中加载用户信息"""
    token = ctx.request.get_cookie('token')
    ctx.user = None
    if token:
        user = User.load_user_from_redis_by_token(token)
        ctx.user = user


@app.before_request
def can_access_api_desc(ctx: AppRequestContext):
    """
    检查用户是否有权限查看api文档（以desc结尾的所有url）

    因为开发文档是比较隐秘的信息，普通用户是没有权限查看的
    """
    path = ctx.request.path
    if isinstance(path, str) and path.endswith('/desc'):
        # if not getattr(ctx, 'user', None):
        if not ctx.user:
            abort(RespCode.error, msg="login first")

        user = ctx.user
        assert isinstance(user, User)
        if not user.can(Permission.admin):
            abort(RespCode.error, msg="permission denied")


@app.after_request
def log_ctx(ctx: AppRequestContext, response: Response):
    app.logger.info(f"method: {ctx.method}, uri: {ctx.uri}, "
                    f"status: {response.status_code}, code: {response.resp_code}, msg: {response.msg}")
    return response
