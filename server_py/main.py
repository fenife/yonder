#!/usr/bin/env python3

"""
api app server
"""

import sys
from app import app


def start():
    host = '0.0.0.0'
    port = 8010
    app.run(host=host, port=port, show_routes=True)


def usage():
    print()
    print(f"sys.argv: {sys.argv}")
    print("usage: ")
    print("  python main.py")
    print()


def main():
    start()


if __name__ == "__main__":
    main()
