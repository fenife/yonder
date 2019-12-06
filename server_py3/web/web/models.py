#!/usr/bin/env python3

from sim.norm import (IntField, VarcharField, Model)
from . import db


class User(Model):
    id = IntField(column_type='int', null=False, primary_key=True, extra="auto_increment")
    name = VarcharField(column_type='varchar(255)')
    # name = VarcharField(column_type='varchar(255)', primary_key=True)

    __database__ = db
    __table__ = 'users'
    __unique_key__ = ('id', 'name')
    __index_key__ = [('id', 'name'), ('name',)]

    @classmethod
    def get_user(cls, uid):
        sql = f"select id, name from users where id = {uid}"
        data = db.select(sql)
        user = data[0] if data else None
        return user
