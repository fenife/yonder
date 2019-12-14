#!/usr/bin/env python3

from functools import wraps
from sim.exceptions import abort
from . import app
from .utils import (load_user_from_redis_by_token, )


@app.before_request
def load_user_to_context(ctx):
    token = ctx.request.get_cookie('token')
    ctx.user = None
    if token:
        user = load_user_from_redis_by_token(token)
        ctx.user = user
