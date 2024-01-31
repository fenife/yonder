#!/usr/bin/env python3

from functools import wraps
from collections import OrderedDict
from sim.context import AppRequestContext


class ApiDescBase(object):
    """api描述文档"""

    # host = "http://127.0.0.1:6070"  # server host
    # 修改/etc/hosts，添加此域名的解析
    host = "http://yonder-search-dev.com:6090"  # server host

    name = ""       # api name
    desc = ""       # api description
    method = []     # api methods
    rule = ""       # api rule(route)
    default_req_headers = [
        # (key, val, desc)
        ('Content-Type', 'application/json', 'body格式类型，默认为json')
    ]

    def __init__(self, ctx: AppRequestContext):
        self.ctx = ctx
        self.url = self.host + self.rule

    def req_headers(self):
        """请求头部"""
        headers = [
            # (key, val, desc)
        ]

        if 'POST' in self.method or 'PUT' in self.method:
            headers += self.default_req_headers

        return headers

    def req_args(self):
        """请求参数，`?`后面的参数，比如： url?a=1&b=2"""
        args = [
            # (key, name, type, default, required, desc)
            # (字段，字段名称，字段类型，默认值，是否必传，备注描述)
        ]
        return args

    def req_body(self):
        """请求body"""
        body = [
            # (key, name, type, default, required, desc)
            # (字段，字段名称，字段类型，默认值，是否必传，备注描述)
        ]
        return body

    @property
    def request(self):
        """api请求描述文档"""
        headers = self.req_headers()
        headers = {
            v[0]: {
                "value": v[1],
                "desc":  v[2],
            }
            for v in headers
        }

        args = self.req_args()
        args = {
            v[0]: {
                "name":     v[1],
                "type":     v[2],
                "default":  v[3],
                "required": v[4],
                "desc":     v[5],
            }
            for v in args
        }

        body = self.req_body()
        body = {
            v[0]: {
                "name":     v[1],
                "type":     v[2],
                "default":  v[3],
                "required": v[4],
                "desc":     v[5],
            }
            for v in body
        }

        req = {
            'headers': headers,
            'args': args,
            'body': body,
        }
        return req

    def resp_headers(self):
        """响应头部"""
        headers = [
            # (key, val, desc)
        ] + self.default_req_headers
        return headers

    @property
    def response(self):
        """api响应描述文档"""
        headers = self.resp_headers()
        headers = {
            v[0]: {
                "value": v[1],
                "desc":  v[2],
            }
            for v in headers
        }

        code = {
            "name": "响应应状态码",
            "desc": "0 表示正确; -1 表示错误",
            "type": "number",
        }

        msg = {
            "name": "状态消息",
            "desc": "请求的错误消息; 正确返回'OK';",
            "type": "string",
        }

        data = {
            "name": "返回的数据",
            "desc": "返回的数据，json格式",
            "type": "json",
        }

        resp = {
            "headers": headers,
            "body": {
                "code": code,
                "data": data,
                "msg": msg,
            }
        }
        return resp

    @property
    def example(self):
        """请求实例，格式自定义"""
        raise NotImplementedError("example method must be implemented")

    def __call__(self, *args, **kwargs):
        resp = OrderedDict()
        resp["method"] = self.method
        resp["rule"] = self.rule
        resp["url"] = self.url
        resp["name"] = self.name
        resp["desc"] = self.desc
        resp["request"] = self.request
        resp["response"] = self.response
        resp["example"] = self.example

        return resp


def api_desc_wrapper():
    """
    把描述文档的class用函数封装起来，方便加到app的路由系统中

    比如:

        from . import app

        @app.route('/api/test/desc')
        @api_desc_wrapper()
        class ApiDesc(ApiDescBase):
            pass

    当请求`/api/test/desc`时，会返回ApiDesc的内容
    """
    def decorator(api_desc_class):
        # @api_cache()
        @wraps(api_desc_class)
        def wrapper(ctx, *args, **kwargs):
            assert issubclass(api_desc_class, ApiDescBase)

            desc = api_desc_class(ctx)
            resp = desc(*args, **kwargs)
            return resp

        return wrapper
    return decorator




