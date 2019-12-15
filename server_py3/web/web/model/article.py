#!/usr/bin/env python3

import json
import hashlib
from sim.exceptions import abort
from sim.norm import (Model, gen_now, IntField, StringField, DatetimeField, TextField)
from .. import app, db, cache_pool
from ..consts import RespCode, Permission, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from ..utils import html_escape, is_ascii


class Article(Model):
    id = IntField(null=False, primary_key=True, extra="auto_increment")
    created_at = DatetimeField(null=True, default=gen_now)
    updated_at = DatetimeField(null=True, default=gen_now, update=gen_now)

    user_id = IntField(null=False, comment="用户ID")
    cate_id = IntField(null=False, comment="分类ID")
    title = StringField(column_type='varchar(255)', null=False, comment="标题")
    content = TextField(null=False, default=None, comment="文章内容")
    # status = IntField(null=False, default=ARTICLE.status.active, comment="文章状态")
    status = IntField(null=False, comment="文章状态")

    __database__ = db
    __table__ = 'articles'
    __unique_key__ = ('title', )
    __index_key__ = [('user_id', ), ('cate_id', ), ]

    @classmethod
    def find_by_title(cls, title):
        sql = f"{cls.__select__} where `title`=?"
        data = cls.select(sql, [title], 1)
        if not data:
            return None

        return cls(**data[0])

    @staticmethod
    def valid_title(title):
        assert isinstance(title, str)

        # prevent xss
        valid_title = html_escape(title)
        if valid_title != title:
            abort(RespCode.error, "name can not contain html special char")

        return valid_title
