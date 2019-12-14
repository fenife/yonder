#!/usr/bin/env python3


class RespCode(object):
    error = -1


class Permission(object):
    """
    目前最多支持16种权限： 0xffff
    每一个二进制位代表一种权限
    """
    admin = 0x01
    write_article = 0x02
    comment = 0x04


class RoleAdmin(object):
    """管理员"""
    id = 1
    name = "admin"
    permissions = 0xffff


class RoleUser(object):
    """普通用户"""
    id = 2
    name = "user"
    permissions = Permission.comment


class Roles(object):
    """所有Role的汇总"""
    _roles = {
        RoleAdmin.id: RoleAdmin,
        RoleUser.id:  RoleUser,
    }

    @classmethod
    def get(cls, role_id):
        r = cls._roles.get(role_id, None)
        return r


class USER(object):

    # 用户登录过期时间
    login_expired = 24 * 60 * 60

    class status(object):
        """用户状态"""
        delete = 0
        active = 1

    class role(object):
        """用户角色id"""
        admin = RoleAdmin.id
        user = RoleUser.id


class CATEGORY(object):
    class status(object):
        delete = 0
        active = 1


class ARTICLE(object):
    class status(object):
        delete = 0
        active = 1
