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

sim_path = os.path.abspath(os.path.join(os.path.dirname(__name__), '..', '..', 'sim'))
print(f"sim_path: {sim_path}")
sys.path.append(sim_path)

# ../../sim dir
from sim.application import Application
from sim.norm import Database
from sim.cache import AppCachePool


# build index
# save data source to file
# save index to file
# search
# api


class SearchIndex(object):
    def __init__(self):
        self.total_index = {}

    def add(self):
        pass

    def get(self):
        pass


total_data = {}     # 建索引的源数据，搜索时会返回这里的内容
total_index = {}    # 索引数据


def get_stopwords():
    with open('./stopwords.txt', encoding='utf-8') as f:
        stopwords = set([l.strip('\n') for l in f.readlines()])

    return stopwords


STOPWORDS = get_stopwords()


def text_to_tokens(text: str):
    """
    把一段内容通过jieba库进行分词，
    记录该词元(token)的位置信息，
    过滤停用词

    :param text: str, utf-8
    :return:     {word: [pos1, pos2, ...], ... }
    """
    if not str:
        return

    tokens = jieba.tokenize(text, mode='search')

    res = {}
    for token in tokens:
        word, start, end = token

        word = word.strip(' ').strip('\n').lower()
        if not word or word in STOPWORDS or word.startswith('#'):
            continue

        if word not in res:
            res[word] = []

        res[word].append(start)

    return res


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
    global total_data
    global total_index

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
        total_index[word] = OrderedDict(
            sorted(total_index[word].items(), key=lambda x: len(x[1]), reverse=True)
        )

    total_data[doc_id] = text


def search_one_word(keyword):

    # {document_id: text, ...}
    global total_data

    # {word: {document_id: [pos1, pos2, ...]}, ...}, ...}
    global total_index

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


def main():
    articles = [
        {
            "id": 1,
            "title": "Python中调用C语言扩展模块hello调用",
            "content": "Python中调用C语言扩展模块hello调用",
        },
        {
            "id": 2,
            "title": "C语言中调用Python模块调用调用",
            "content": "C语言中调用Python模块调用调用",
        },

    ]

    for article in articles:
        build_index(article['id'], article['title'])

    pprint.pprint(total_data)
    pprint.pprint(total_index)

    search('扩展')


if __name__ == '__main__':
    main()
