#!/usr/bin/env python3

"""
api app server
"""


import sys

from app import app, db
from app.model import User, Category, Article, create_admin_user


def add_admin():
    return create_admin_user()


def start():
    host = '0.0.0.0'
    port = 8010
    app.run(host=host, port=port, show_routes=True)


def usage():
    print()
    print(f"sys.argv: {sys.argv}")
    print("usage: %prog [options]")
    print("  python main.py [admin]")
    print("  [admin]: create super admin user")
    print()


def main():
    if len(sys.argv) > 2:
        usage()
        return

    if len(sys.argv) == 2:
        if sys.argv[1] == 'admin':
            add_admin()
        else:
            usage()
            return
    else:
        start()


if __name__ == "__main__":
    main()
