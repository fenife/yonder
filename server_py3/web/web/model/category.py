#!/usr/bin/env python3

import json
import hashlib
from sim.exceptions import abort
from sim.norm import (Model, gen_now, IntField, StringField, DatetimeField, TextField)
from .. import app, db, cache_pool
from ..consts import RespCode, Permission, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from ..utils import html_escape, is_ascii


class Category(Model):
    id = IntField(null=False, primary_key=True, extra="auto_increment")
    created_at = DatetimeField(null=True, default=gen_now)
    # updated_at = DatetimeField(null=False, auto_now=True, extra="on update current_timestamp")
    updated_at = DatetimeField(null=True, default=gen_now, update=gen_now)

    name = StringField(null=False, comment="分类名称")
    # status = IntField(null=False, default=CATEGORY.status.active, comment="分类状态")
    status = IntField(null=False, comment="分类状态")

    __database__ = db
    __table__ = 'categories'
    __unique_key__ = ('name', )
    # __index_key__ = [('user_id', ), ('cate_id', ), ]
