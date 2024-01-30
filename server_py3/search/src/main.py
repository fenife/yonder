#!/usr/bin/env python3

"""
api app server
"""


import sys
from ses.engine.store import store_load, print_data_and_index

from ses import app


def load_search_data():
    try:
        store_load()
        app.logger.info("load search data success")
    except Exception as e:
        app.logger.exception("load search data failed")
        sys.exit()


def start():
    host = '127.0.0.1'
    port = 6090
    app.run(host=host, port=port, show_routes=True)


def usage():
    print()
    print("usage: %prog [options]")
    print("  python main.py")
    print()


def main():
    load_search_data()
    start()


if __name__ == "__main__":
    main()
