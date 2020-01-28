#!/usr/bin/env python3

"""
api app server
"""


import sys

from ses import app, db


def start():
    host = '127.0.0.1'
    port = 6090
    app.run(host=host, port=port, show_routes=True)


def usage():
    print()
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
