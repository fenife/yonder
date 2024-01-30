#!/usr/bin/env python3


class Dict(dict):
    def __init__(self, *args, **kwargs):
        super(Dict, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"`Dict` object has no attribute `{item}`")

    def __setattr__(self, key, value):
        self[key] = value


def html_escape(s):
    r = s.replace('&', '&amp;') \
         .replace('>', '&gt;')  \
         .replace('<', '&lt;')  \
         .replace("'", '&#39;') \
         .replace('"', '&#34;')
    return r


def is_ascii(s):
    return len(s) == len(s.encode())
