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

from web import app
from web.model import User, Category, Article, create_admin_user


def table_migrate():
    User.table_drop()
    User.table_create()
    User.table_show()

    Category.table_drop()
    Category.table_create()
    User.table_show()

    Article.table_drop()
    Article.table_create()
    User.table_show()


def add_admin():
    return create_admin_user()


def main():
    host = '0.0.0.0'
    port = 6070
    app.run(host=host, port=port, debug=True)
    # app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    argv = sys.argv
    if argv[-1] == 'migrate':
        table_migrate()
    elif argv[-1] == 'admin':
        add_admin()
    else:
        main()
