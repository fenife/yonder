#!/usr/bin/env python3

"""
ses: search service

tf: term frequency
"""

import os
import sys
import pprint

engine_path = os.path.abspath(
    os.path.join(os.path.dirname(__name__), '..', 'src')
)
print(f"engine_path: {engine_path}")
print(f"cur: {os.path.abspath('.')}")
sys.path.append(engine_path)

from ses.engine.build import total_data, total_index, build
from ses.engine.store import store_save, store_load, print_data_and_index
from ses.engine.query import search


def main():
    articles = [
        {
            "id": 1,
            "title": "Python中调用C语言扩展模块machine learning调用",
            # "content": "Python中调用C语言扩展模块hello调用",
        },
        {
            "id": 2,
            "title": "C语言中调用Python模块调用ai调用",
            # "content": "C语言中调用Python模块调用调用",
        },

    ]

    for article in articles:
        build(article)
        store_save()
        # build_index(article['id'], article['title'])

    print_data_and_index()

    keyword = "C调用"
    res = search(keyword)

    print('-' * 50)
    print(f"keyword: '{keyword}', res:")
    pprint.pprint(res)


if __name__ == '__main__':
    main()
