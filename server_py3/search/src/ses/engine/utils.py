#!/usr/bin/env python3

import os
import jieba


NGRAM_N_MIN = 2      # N-Gram, 分词的最小长度
NGRAM_N_MAX = 5      # N-Gram, 分词的最大长度


def get_stopwords():
    fn = f"{os.path.dirname(__file__) or '.'}/stopwords.txt"
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
    def add_token(res, token):
        word, start, end = token

        word = word.strip(' ').strip('\n').lower()
        if not word or word in STOPWORDS:
            return

        if word not in res:
            res[word] = []

        res[word].append(start)

    if not text:
        return

    tokens = jieba.tokenize(text, mode='search')

    res = {}
    for token in tokens:
        word, start, end = token
        add_token(res, token)

        # N-Gram
        if len(word) >= NGRAM_N_MIN:
            ngram_tokens = word_ngrams(word)

            # tk, ngram token: (word, start, end)
            for tk in ngram_tokens:
                add_token(res, tk)

    return res


def word_ngrams(word, ngram_range=(NGRAM_N_MIN, NGRAM_N_MAX)):
    """
    Turn tokens into a sequence of n-grams
    来自sklearn中CountVectorizer用于N-Gram的方法

    :param word:
    :param ngram_range:
    :return:
    """
    min_n, max_n = ngram_range
    tokens = []
    if max_n <= 1:
        return []

    original_tokens = word
    n_original_tokens = len(original_tokens)
    # n: gram range
    for n in range(min_n, min(max_n + 1, n_original_tokens + 1)):
        # split word
        for i in range(n_original_tokens - n + 1):
            start, end = i, i + n
            token = original_tokens[start: end]
            tokens.append((token, start, end))

    return tokens


def _test():
    text = "python"
    tokens = text_to_tokens(text)
    # tokens = word_ngrams(text)
    print(tokens)


if __name__ == '__main__':
    _test()
