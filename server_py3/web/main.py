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


def main():
    host = '0.0.0.0'
    port = 6070
    app.run(host=host, port=port, debug=True)
    # app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()
