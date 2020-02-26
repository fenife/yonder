#!/usr/bin/env python3

import sys
import logging
import json
import requests
import datetime
from logging.handlers import TimedRotatingFileHandler

from wes import db


# logger = logging.getLogger('yonder.build_index')
logger = logging.getLogger()


def setup_logger(logger):

    # logger配置
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)-5s]"
        " [%(threadName)s]"
        " [%(name)s]"
        " [%(filename)s:%(funcName)s:%(lineno)d]"
        " -- %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    log_level = logging.DEBUG

    # 指定日志的最低输出级别
    logger.setLevel(log_level)

    # 控制台日志
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # 写日志到文件中
    fn = "logs/build_index.log"
    fh = TimedRotatingFileHandler(filename=fn, when='MIDNIGHT')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


def init():
    setup_logger(logger)

    # sim_logger = logging.getLogger('sim')
    # sim_logger.handlers = []
    # setup_logger(sim_logger)


def build_search_index():
    """
    更新索引
    :return:
    """

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

    for article in items:
        r = call_ses_update(article)


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
        "title": "aafdsfdsa",
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
