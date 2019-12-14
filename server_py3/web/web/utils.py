#!/usr/bin/env python3


def html_escape(s):
    r = s.replace('&', '&amp;') \
         .replace('>', '&gt;')  \
         .replace('<', '&lt;')  \
         .replace("'", '&#39;') \
         .replace('"', '&#34;')
    return r


def is_ascii(s):
    return len(s) == len(s.encode())
