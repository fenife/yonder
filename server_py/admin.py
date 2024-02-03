#!/usr/bin/env python3

"""
创建管理员用户
"""

from app.model import create_admin_user


def usage():
    print()
    print("create super admin user")
    print("usage: ")
    print("  python admin.py")
    print()


def main():
    create_admin_user()


if __name__ == "__main__":
    main()
