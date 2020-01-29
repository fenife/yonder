#!/user/bin/env python3

from functools import wraps
import json

from sim.exceptions import abort
from sim.context import AppRequestContext
from . import app, cache_pool


API_CACHE_EXPIRED = 10 * 60


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
