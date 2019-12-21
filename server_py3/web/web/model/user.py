#!/usr/bin/env python3

import json
import hashlib
from sim.exceptions import abort
from sim.norm import (Model, gen_now, IntField, StringField, DatetimeField, TextField)
from .. import app, db, cache_pool
from ..consts import RespCode, Permission, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from ..utils import html_escape, is_ascii


class User(Model):
    id = IntField(null=False, primary_key=True, extra="auto_increment")
    created_at = DatetimeField(null=True, default=gen_now)
    # updated_at = DatetimeField(null=False, auto_now=True, extra="on update current_timestamp")
    updated_at = DatetimeField(null=True, default=gen_now, update=gen_now)

    name = StringField(column_type='varchar(255)', null=False, comment="用户名")
    password = StringField(null=False, comment="密码")
    role_id = IntField(null=False, comment="角色ID")
    # status = IntField(null=False, default=USER.status.active, comment="用户状态")
    status = IntField(null=False, comment="用户状态")

    __database__ = db
    __table__ = 'users'
    __unique_key__ = ('name', )
    # __index_key__ = [('id', 'name'), ('name',)]

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # self.role = self.get_role()
        # self.password = '***'

    @property
    def role(self):
        if 'role_id' in self and self.role_id is not None:
            role = Roles.get(self.role_id)
            return role

        return None

    def can(self, permissions):
        if not self.role:
            return False

        r = self.role.permissions & permissions == permissions
        return r

    def is_admin(self):
        return self.can(Permission.admin)

    @staticmethod
    def gen_password_hash(password):
        m = hashlib.md5()
        # m.update(db.app.config["SECRET_KEY"].encode('utf-8'))
        # m.update(password.encode('utf-8'))
        s = f"{db.app.config['SECRET_KEY']}-{password}"
        m.update(s.encode('utf-8'))
        h = m.hexdigest()
        return h

    def verify_password(self, password):
        password_hash = self.gen_password_hash(password)
        return self.password == password_hash

    def gen_session_token(self):
        m = hashlib.md5()
        s = f"{db.app.config['SECRET_KEY']}-{self.id}-{self.name}-{self.password}"
        m.update(s.encode('utf-8'))
        token = m.hexdigest()
        return token

    @classmethod
    def find_by_name(cls, username):
        sql = f"{cls.__select__} where `name`=?"
        data = cls.__database__.select(sql, [username], 1)
        if not data:
            return None

        return cls(**data[0])

    def without_password(self):
        return {k: v for k, v in self.items() if k != 'password'}

    @staticmethod
    def valid_username(name):
        assert isinstance(name, str)
        if ' ' in name:
            abort(RespCode.error, "username can not contain blank space")

        if not (4 <= len(name) <= 20):
            abort(RespCode.error, "username len must between 4 and 20")

        # prevent xss
        valid_name = html_escape(name)
        if valid_name != name:
            abort(RespCode.error, "username can not contain html special char")

        # if not is_ascii(user.name):
        #     abort(RespCode.error, "no-ascii char is not supported for username yet")

        # if not re.match(r"^[a-zA-Z\_][0-9a-zA-Z\_]{3, 19}$", user.name):
        # app.logger.error(f"re not match for username: {user.name}")
        # abort(RespCode.error, "username is invalid")

        return name

    @staticmethod
    def valid_password(password):
        if ' ' in password:
            abort(RespCode.error, "password can not contain blank space")

        if not (3 <= len(password) <= 20):
            abort(RespCode.error, "password len must between 3 and 20")

        if not is_ascii(password):
            abort(RespCode.error, "password can not contain no-ascii char")

        return password

    @staticmethod
    def save_user_to_redis_by_token(user, token):
        assert isinstance(user, User)
        with cache_pool.get() as cache:
            key = f"token:{token}"
            val = json.dumps(user, default=str).encode('utf-8')
            expired = app.config.get("LOGIN_EXPIRED")
            cache.set(key, val, ex=expired)

    @staticmethod
    def load_user_from_redis_by_token(token):
        with cache_pool.get() as cache:
            key = f"token:{token}"
            val = cache.get(key)
            if not val:
                return

            data = json.loads(val)
            user = User(**data)
            return user

    @staticmethod
    def del_user_from_redis(token):
        with cache_pool.get() as cache:
            key = f"token:{token}"
            app.logger.debug(token)
            cache.delete(key)


def create_admin_user():
    username = app.config['ADMIN_USERNAME']
    password = app.config['ADMIN_PASSWORD']
    admin = User()
    admin.name = username
    admin.password = admin.gen_password_hash(password)
    admin.status = USER.status.active
    admin.role_id = USER.role.admin
    admin.save()
    print('admin user:', admin.without_password())
