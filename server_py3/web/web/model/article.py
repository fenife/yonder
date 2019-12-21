#!/usr/bin/env python3

import json
import hashlib
from sim.exceptions import abort
from sim.norm import (Model, gen_now, IntField, StringField, DatetimeField, TextField)
from .. import app, db, cache_pool
from ..consts import RespCode, Permission, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from ..utils import html_escape, is_ascii
from .user import User
from .category import Category


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

    @classmethod
    def get_with_more_detail(cls, pk):
        article = cls.find(pk)
        if not article:
            return None

        user_id = article.user_id
        user = User.find(user_id)
        if not user:
            app.logger.error(f"can not get category of article: {article.id}, user_id: {user_id}")
            # abort(RespCode.error, f"can not get user")
            article.user = None
        else:
            article.user = user.without_password()

        cate_id = article.cate_id
        cate = Category.find(cate_id)
        if not cate:
            app.logger.error(f"can not get category of article: {article.id}, cate_id: {cate_id}")
            # abort(RespCode.error, f"can not get category")

        article.category = cate

        return article

    def get_pre(self):
        sql = f"""
        {self.__select__} where `{self.__primary_key__}` < ? 
        order by `{self.__primary_key__}` desc"""

        data = self.select(sql, [self.id], 1)
        if not data:
            return None

        return Article(**data[0])

    def get_next(self):
        sql = f"""
        {self.__select__} where `{self.__primary_key__}` > ? 
        order by `{self.__primary_key__}` asc"""

        # sql = f"{self.__select__} where `{self.__primary_key__}` > ?"

        data = self.select(sql, [self.id], 1)
        if not data:
            return None

        return Article(**data[0])

    @staticmethod
    def valid_title(title):
        assert isinstance(title, str)

        # prevent xss
        valid_title = html_escape(title)
        if valid_title != title:
            abort(RespCode.error, "name can not contain html special char")

        return valid_title
