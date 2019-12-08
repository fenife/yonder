#!/usr/bin/env python3

from sim.norm import (IntField, VarcharField, Model)
from . import db


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
    id = IntField(column_type='int(11)', null=False, primary_key=True, extra="auto_increment")
    name = VarcharField(column_type='varchar(255)')
    password = VarcharField(column_type='varchar(255)')
    role = IntField(column_type='int(11)')
    status = IntField(column_type='int(11)')
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
