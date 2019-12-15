#!/user/bin/env python3

from functools import wraps
from sim.exceptions import abort
from .model import User
from .consts import RespCode


def permission_required(permission):
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
