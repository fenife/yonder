#!/usr/bin/env python3

from test_app import db
from sim.norm import (Model, gen_now, IntField, StringField, DatetimeField, )
from sim.pretty import dictList2Table


"""
+------------+------------------+------+-----+---------+----------------+
| Field      | Type             | Null | Key | Default | Extra          |
+------------+------------------+------+-----+---------+----------------+
| id         | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| created_at | timestamp        | YES  |     | NULL    |                |
| updated_at | timestamp        | YES  |     | NULL    |                |
| deleted_at | timestamp        | YES  | MUL | NULL    |                |
| name       | varchar(255)     | NO   | MUL | NULL    |                |
| passwd     | varchar(255)     | NO   |     | NULL    |                |
| role       | int(11)          | NO   |     | NULL    |                |
| status     | int(11)          | NO   |     | NULL    |                |
+------------+------------------+------+-----+---------+----------------+

CREATE TABLE `users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `passwd` varchar(255) NOT NULL,
  `role` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_users_deleted_at` (`deleted_at`),
  KEY `idx_users_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4

CREATE TABLE `u1` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

insert into u1(id) values(1);
"""


class User(Model):
    id = IntField(null=False, primary_key=True, extra="auto_increment")
    deleted_at = DatetimeField(null=True)
    created_at = DatetimeField(null=True, default=gen_now)
    # updated_at = DatetimeField(null=False, auto_now=True, extra="on update current_timestamp")
    updated_at = DatetimeField(null=True, default=gen_now, update=gen_now)

    name = StringField(column_type='varchar(255)', null=False)
    password = StringField(null=False)
    role = IntField(null=False)
    # status = IntField(column_type='int(11)')
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


def _test_create():
    User.table_drop()
    User.table_create()

    User.table_show()


def _test_insert():
    # create, insert
    user = User(name='u1', password="p1", role=1)
    user.save()

    User.print_all()


def _test_update():
    u1 = User.find(1)
    if u1:
        print(dictList2Table([u1]))

    u1.name = 'user1'
    u1.role = 2
    u1.modify()

    User.print_all()


def _test():
    _test_create()
    _test_insert()
    _test_update()


def _test_bak():

    # print([User.find(16)])

    u2 = User(id=15, name='user2', password='password2', role=3)
    u2.update()

    sql = "select * from users"
    data = db.select(sql)
    print(dictList2Table(data))


if __name__ == "__main__":
    _test()
