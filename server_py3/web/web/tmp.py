#!/usr/bin/env python3

from . import app, db
from sim.norm import (Model, gen_now, IntField, StringField, TextField, DatetimeField, )
from sim.pretty import dictList2Table


class Category(Model):
    id = IntField(null=False, primary_key=True, extra="auto_increment")
    created_at = DatetimeField(null=True, default=gen_now)
    # updated_at = DatetimeField(null=False, auto_now=True, extra="on update current_timestamp")
    updated_at = DatetimeField(null=True, default=gen_now, update=gen_now)

    name = StringField(null=False, comment="分类名称")
    status = IntField(null=False, comment="分类状态")       # todo: default ?

    __database__ = db
    __table__ = 'categories'
    __unique_key__ = ('name', )
    # __index_key__ = [('user_id', ), ('cate_id', ), ]


class Article(Model):
    id = IntField(null=False, primary_key=True, extra="auto_increment")
    created_at = DatetimeField(null=True, default=gen_now)
    updated_at = DatetimeField(null=True, default=gen_now, update=gen_now)

    user_id = IntField(null=False, comment="用户ID")
    cate_id = IntField(null=False, comment="分类ID")
    title = StringField(column_type='varchar(255)', null=False, comment="标题")
    content = TextField(null=True, default=None, comment="文章内容")
    status = IntField(null=False, comment="文章状态")       # todo: default ?

    __database__ = db
    __table__ = 'articles'
    __unique_key__ = ('title', )
    __index_key__ = [('user_id', ), ('cate_id', ), ]
