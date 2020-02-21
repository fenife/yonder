#!/usr/bin/env python3

"""
数据索引存储层

保存所建的索引和源数据，app重启后可恢复
"""

import os
import sys
import json
import pprint

store_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data')
)
print('store_path:', store_path)

data_path = store_path + '/data.txt'

index_path = store_path + '/index.txt'


# 建索引的源数据，搜索时会返回这里的内容
# {document_id: text, ...}
total_data = {}

# 索引数据
# {word: {document_id: [pos1, pos2, ...]}, ...}, ...}
total_index = {}


def store_save():
    try:
        if not os.path.exists(store_path):
            os.mkdir(store_path)

        print("data to save:")
        pprint.pprint(total_data)
        with open(data_path, 'w') as f:
            json.dump(total_data, f, indent=1)

        with open(index_path, 'w') as f:
            json.dump(total_index, f)

    except Exception as e:
        print('save data for search failed')
        raise


def store_load():
    global total_data
    global total_index

    try:
        if os.path.exists(data_path):
            with open(data_path, 'r') as f:
                total_data.update(json.load(f))

        if os.path.exists(index_path):
            with open(index_path, 'r') as f:
                total_index.update(json.load(f))

        print('load data for search success')

    except Exception as e:
        print('load data for search failed')
        raise


def print_data_and_index():
    global total_data
    global total_index

    print("-" * 20, 'data and index:')
    pprint.pprint(total_data)
    pprint.pprint(total_index)


def _test():
    from collections import OrderedDict
    global total_data
    global total_index

    total_data = {
        1: 'Python中调用C语言扩展模块hello调用',
        2: 'C语言中调用Python模块调用调用'
    }
    total_index = {
        'c语言': {1: [9], 2: [0]},
        'python': {1: [0], 2: [6]},
        '中': {1: [6], 2: [3]},
        '扩展': {1: [12]},
        '模块': {1: [14], 2: [12]},
        '语言': {1: [10], 2: [1]},
        '调用': {1: [7, 21], 2: [4, 14, 16]}
    }

    store_save()

    store_load()


if __name__ == "__main__":
    _test()
