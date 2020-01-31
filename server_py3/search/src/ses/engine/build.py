#!/usr/bin/env python3

"""
ses: search service

tf: term frequency
"""

import os
import sys
import pprint

from .store import total_data, total_index, store_save
from .utils import text_to_tokens
from ses import app


def build_index(doc_id, text):
    """
    :param doc_id: document_id, must be unique in global
    :param text: str, utf-8
    :return:
    1. save source data (global)
        {document_id: text, ...}
    2. global index
        {word: {document_id: [pos1, pos2, ...]}, ...}, ...}
    """

    # tokens: {word: [pos1, pos2, ...], ... }
    tokens = text_to_tokens(text)

    for word, pos_list in tokens.items():
        if word not in total_index:
            total_index[word] = {}

        # doc_id 应该是唯一的，而且tokens中的词元是已经合并过的，
        # 同一个词元在同一个doc_id中应该是不会出现多次的，
        # 所以这里直接用赋值运算，而不必再合并
        total_index[word][doc_id] = pos_list

        # 同一个词元，其docs先按词频(tf)排序
        # total_index, eg:
        #   {'Python': {1: [7, 21], 2: [4, 14, 16]} }
        #
        # lambda x, eg:
        #   (doc_id, [pos1, pos2, ...])
        #   (文档唯一标识id，[词元在文档中出现的起始位置, ...])
        #   (1, [7, 21])
        #
        # len(x[1]), 该词元在文档中出现了多少次（词频）
        # total_index[word] = OrderedDict(
        #     sorted(total_index[word].items(), key=lambda x: len(x[1]), reverse=True)
        # )


def build(article):
    """
    传入文章内容，建立索引，并保存该内容
    :param article:
    {
        "id": 2,
        "title": "aaaa",
        "created_at": "2019-12-20 23:47:37",
        "updated_at": "2020-01-12 15:55:58",
        "user_id": 1,
        "user_name": "admin",
        "cate_id": 1,
        "cate_name": "aaa"
    }
    :return:
    """
    try:
        doc_id, text = article['id'], article['title']
    except Exception as e:
        app.logger.exception("field `id`, `title` not found in article")
        raise

    try:
        build_index(doc_id, text)
    except Exception as e:
        app.logger.exception("build index failed")
        raise

    total_data[doc_id] = article
