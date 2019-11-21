#!/usr/bin/env python3

from .http import HTTP_STATUS_CODES


DB_STATUS_CODES = {
    -100: "db config error",
    -200: "db connect error",
}


_status_codes = {}

_status_codes.update(HTTP_STATUS_CODES)

_status_codes.update(DB_STATUS_CODES)


def code2name(code):
    n = _status_codes.get(code, "Unknown Error")
    return n


def code2status(code):
    """
    根据状态码得到完整的状态字符串
    :param code: int
    :return: code + name
        eg: 200 => "200 OK"
    """
    s = str(code) + " " + code2name(code)
    return s
