#!/user/bin/env python3

from functools import wraps
import json

from lime.exceptions import abort
from lime.context import AppRequestContext
from app.model import User
from app.consts import RespCode
from app import app, cache_pool


API_CACHE_EXPIRED = 10


def permission_required(permission):
    """看用户是否具有某种权限"""
    def decorator(func):
        @wraps(func)
        def wrapper(ctx, *args, **kwargs):
            if not getattr(ctx, 'user', None):
                abort(RespCode.error, msg="login first")

            user = ctx.user
            assert isinstance(user, User)
            if not user.can(permission):
                abort(RespCode.error, msg="permission denied")

            return func(ctx, *args, **kwargs)

        return wrapper
    return decorator


def login_required():
    """login required"""
    def decorator(func):
        @wraps(func)
        def wrapper(ctx, *args, **kwargs):
            if not getattr(ctx, 'user', None):
                # abort(RespCode.error, msg="permission denied")
                abort(RespCode.error, msg="login first")

            return func(ctx, *args, **kwargs)

        return wrapper
    return decorator


def api_cache(ex=API_CACHE_EXPIRED):
    """cache app api result"""
    def decorator(func):
        @wraps(func)
        def wrapper(ctx: AppRequestContext, *args, **kwargs):
            with cache_pool.get() as cache:
                key = ctx.uri
                val = cache.get(key)
                if val:
                    app.logger.debug(f"get resp from cache, key: `{key}`")
                    # resp = json.loads(val)
                    resp = val
                    return resp

                resp = func(ctx, *args, **kwargs)
                val = json.dumps(resp, default=str)
                cache.set(key, val, ex=ex)
                return resp

        return wrapper
    return decorator
