#!/usr/bin/env python3

"""
创建、更新文章的搜索索引
"""

import os
import sys
import logging
import json
import requests
import datetime

sim_path = os.path.abspath(os.path.join(os.path.dirname(__name__), '..', '..', 'sim'))
sys.path.append(sim_path)

from sim.log import setup_logger
from wes import db

log_name = os.path.basename(__file__).split('.')[0]
logger = logging.getLogger(log_name)


def init():
    for lgr in [logger]:
        setup_logger(lgr, log_file="/work/yonder/server_py3/aps/logs/build_index.log")


def build_search_index():
    """
    更新索引
    :return:
    """
    logger.info('start to build index')
    sql = f"""
    select 
        a.id, a.title, a.created_at, a.updated_at, 
        a.user_id, b.name as user_name,
        a.cate_id, c.name as cate_name
    from articles a
    inner join users b on a.user_id = b.id
    inner join categories c on a.cate_id = c.id"""
    items = db.select(sql)
    if not items:
        raise Exception(f"can not get articles")

    success = 0
    failed = []
    for article in items:
        resp = call_ses_update(article)
        if not resp or resp['code'] != 0:
            failed.append(article["id"])
        else:
            success += 1

    logger.info(f"end to build index, success: {success}, failed: {failed}")


def call_ses_update(article):
    """
    调用搜索服务的接口更新索引
    :param article:
    {
        "title": "test",
        "id": 2
    }
    """
    # http://127.0.0.1:6090/search/query?kw=py&page=1&limit=2
    url = "http://127.0.0.1:6090/search/index/update"
    headers = {
        "Content-Type": "application/json",
    }

    # 解决requests报错：Object of type 'datetime' is not JSON serializable
    for k, v in article.items():
        if isinstance(v, datetime.datetime):
            article[k] = str(v)

    resp = requests.post(url, json=article, headers=headers, timeout=60)
    res = resp.json()
    return res


def call_ses_query(kw, page=None, limit=None):
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


def test():
    article = {
        "id": 1,
        "title": "aafdsfdse",
        "content": "afadasdf",
        "updated_at": datetime.datetime(2020, 2, 26, 17, 27, 42),
        "cate_id": 2
    }
    for k, v in article.items():
        if isinstance(v, datetime.datetime):
            article[k] = str(v)
    print(call_ses_update(article))

    # print(call_ses_query(kw='aa'))


def main():
    init()
    build_search_index()


if __name__ == "__main__":
    main()
