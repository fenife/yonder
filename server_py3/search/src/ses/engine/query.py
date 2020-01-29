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
    total_docs = set()
    tokens = text_to_tokens(keyword)

    for token in tokens.keys():
        # docs: {document_id: [pos1, pos2, ...]}, ...}
        docs = search_one_word(token)
        print('-' * 10, token, docs)
        if not docs:
            continue

        # 取交集
        if not total_docs:
            total_docs = set(docs.keys())
        else:
            total_docs &= set(docs.keys())

    pprint.pprint(total_docs)
    res = [total_data.get(doc_id) for doc_id in total_docs]
    pprint.pprint(res)

