#!/usr/bin/env python3

"""
ses: search service

tf: term frequency
"""

import os
import sys
import jieba
import pprint
from collections import OrderedDict

from .utils import text_to_tokens
from .build import total_index, total_data


def search_one_word(keyword):

    # total_data
    # {document_id: text, ...}

    # total_index
    # {word: {document_id: [pos1, pos2, ...]}, ...}, ...}

    if keyword not in total_index:
        return {}

    # 默认按词频排序
    docs = total_index.get(keyword)
    return docs


def search(keyword):
    indexes = {}
    doc_ids = OrderedDict()

    # 分词
    tokens = text_to_tokens(keyword)

    # 索引查询
    for token in tokens.keys():
        # docs: {document_id: [pos1, pos2, ...]}, ...}
        docs = search_one_word(token)
        if not docs:
            continue

        indexes[token] = docs
        # 结果去重并排序
        # doc_ids.update(set(docs.keys()))
        doc_ids.update([(doc_id, True) for doc_id in docs.keys()])

    # 获取查询到的源数据
    res = [total_data.get(doc_id) for doc_id in doc_ids.keys()]

    return res

