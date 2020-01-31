#!/usr/bin/env python3

import os
import jieba


def get_stopwords():
    fn = f"{os.path.dirname(__file__)}/stopwords.txt"
    with open(fn, encoding='utf-8') as f:
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


