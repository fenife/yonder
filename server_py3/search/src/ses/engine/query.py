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

from .store import total_data, total_index, load
from .utils import text_to_tokens


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


def rank_results(indexes):
    """
    同一个词元，其docs先按词频(tf)排序
    不同的词元可能会查询到同一个文档上，
    同一个文档，根据不同词元的词频(tf)排序

    :param indexes:
        {词元: {文档唯一标识id: [词元在文档中出现的起始位置, ...}, ...)
        {word: {doc_id: [pos1, pos2, ...]}, ...}, ...}
        {'Python': {1: [7, 21], 2: [4, 14, 16]} }
    :return:
    """

    # {doc_id: (token, len(pos_list)), ... }
    # {doc_id: (token, tf), ... }
    merge_docs = {}

    for token, docs in indexes.items():
        for doc_id, pos_list in docs.items():
            if doc_id not in merge_docs:
                # 该文档还没有在查询列表中
                merge_docs[doc_id] = (token, len(pos_list))
            else:
                # 该文档还已经在查询列表中
                # 如果当前词元的词频更高，则更新该文档的词频最大值
                if len(pos_list) > merge_docs[doc_id][1]:
                    merge_docs[doc_id] = (token, len(pos_list))

    # 按词频排序
    # len(pos_list), 该词元在文档中出现了多少次（词频）
    # {doc_id: (token, len(pos_list)), ... }
    # eg: OrderedDict([(2, ('调用', 3)), (1, ('调用', 2))])
    sort_docs = OrderedDict(
        # lambda x: (doc_id, (token, len(pos_list))
        sorted(merge_docs.items(), key=lambda x: x[1][1], reverse=True)
    )
    pprint.pprint((sort_docs))

    doc_ids = sort_docs.keys()
    return doc_ids


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
        # doc_ids.update([(doc_id, True) for doc_id in docs.keys()])

    doc_ids = rank_results(indexes)

    # 获取查询到的源数据
    res = [total_data.get(doc_id) for doc_id in doc_ids]

    return res

