#!/usr/bin/env python

import re


def index():
    print('index page')


def hello():
    print('hello page')


def error():
    print('error page')


_urls = {
    '/index': index,
    '/hello': hello,
    '/hello/': hello,
    '/error': error,
    '/error/': error,
    '/error/500': error,
}

urls = {
    '/index': 'index',
    '/hello': 'hello',
    '/hello/': 'hello',
    '/error': 'error',
    '/error/': 'error',
    '/error/500': 'error',
}

path = '/hello'


class _re_subm_proxy:
    def __init__(self):
        self.match = None

    def __call__(self, match):
        """
        :param match: http request path
        :return:
        """
        self.match = match
        return ''

def re_subm(pat, repl, string):
    """
    like re.sub, but returns the replacement and the match object

    >>> urls = ('/web.py', 'source')
    >>> class source:
    ...     pass

    >>> for url, ofn in urls:
    ...     fn, result = re_subm('^'+url+'$', ofn, context.path)

    :param pat: re pattern, ef: '^hello&'
    :param repl: view handler class name, eg: 'index'
    :param string: http request path
    """
    print('-' * 30)

    r = re.compile(pat)
    proxy = _re_subm_proxy()
    rr = r.sub(proxy.__call__, string)

    print('>>', rr)
    fn, result = r.sub(repl, string), proxy.match

    print(fn, result)

    return fn, result


for url, handler in urls.items():
    pat = '^' + url + '$'
    # r = re.compile(pat)
    # r.sub(handler.__name__, path)
    fn, ret = re_subm(pat, handler, path)


