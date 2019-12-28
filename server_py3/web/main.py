#!/usr/bin/env python3

"""
web api app

todo:
db
models
middleware
auth
"""


import sys
import os
import optparse

from web import app, db
from web.model import User, Category, Article, create_admin_user


def table_backup():
    sql = "rename table users to users_bak;"
    db.execute(sql)

    sql = "rename table categories to categories_bak;"
    db.execute(sql)

    sql = "rename table articles to articles_bak;"
    db.execute(sql)


def table_recovery():
    sql = "rename table users_bak to users;"
    db.execute(sql)

    sql = "rename table categories_bak to categories;"
    db.execute(sql)

    sql = "rename table articles_bak to articles;"
    db.execute(sql)


def table_drop():
    User.table_drop()
    Category.table_drop()
    Article.table_drop()


def recreate_table_user():
    User.table_drop()
    User.table_create()
    User.table_show()


def recreate_table_category():
    Category.table_drop()
    Category.table_create()
    Category.table_show()


def recreate_table_article():
    Article.table_drop()
    Article.table_create()
    Article.table_show()


def table_migrate():
    recreate_table_user()
    recreate_table_category()
    recreate_table_article()


def add_admin():
    return create_admin_user()


def start():
    host = '0.0.0.0'
    port = 6070
    app.run(host=host, port=port)


def parse_input():
    tables = ['user', 'category', 'article']
    parser = optparse.OptionParser("usage: %prog [options]")

    parser.add_option(
        '-m', "--migrate", action="store_true", dest="migrate", default=False,
        help="migrate(create) new tables: users, categories, articles"
    )

    parser.add_option(
        '-t', "--table", choices=tables, dest="table",
        help="recreate table, only used when `-m` option not existed"
    )

    parser.add_option(
        '-s', '--admin', action="store_true", dest="admin", default=False,
        help="create admin user of app web"
    )
    (options, args) = parser.parse_args()
    print(f"options: {options}")
    return options


def _main():
    opts = parse_input()

    # table_drop()
    # table_recovery()

    if opts.migrate:
        table_backup()
        table_migrate()
    elif opts.table:
        table_backup()
        if opts.table == 'user':
            recreate_table_user()
        elif opts.table == 'category':
            recreate_table_category()
        elif opts.table == 'article':
            recreate_table_article()

    elif opts.admin:
        add_admin()

    else:
        start()


def main():
    argv = sys.argv
    if argv[-1] == 'migrate':
        table_migrate()
    elif argv[-1] == 'user':
        recreate_table_user()
    elif argv[-1] == 'category':
        recreate_table_category()
    elif argv[-1] == 'article':
        recreate_table_article()
    elif argv[-1] == 'admin':
        add_admin()
    else:
        start()


if __name__ == "__main__":
    main()
