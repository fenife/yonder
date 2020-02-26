#!/usr/bin/env python3

import requests


def call_ses_query(kw, page, limit):
    """调用搜索服务的接口获取搜索结果"""
    # http://127.0.0.1:6090/search/query?kw=py&page=1&limit=2
    url = "http://127.0.0.1:6090/search/query"
    url += f"?kw={kw}"
    if page:
        url += f"&page={page}"

    if limit:
        url += f"&limit={limit}"

    resp = requests.get(url)
    res = resp.json()
    return res

