#!/usr/bin/env python3

from functools import wraps
from sim.exceptions import abort
from sim.context import AppRequestContext
from . import app
from .model import User


@app.before_request
def load_user_to_context(ctx: AppRequestContext):
    token = ctx.request.get_cookie('token')
    ctx.user = None
    if token:
        user = User.load_user_from_redis_by_token(token)
        ctx.user = user
