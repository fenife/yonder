#!/usr/bin/env python3


from http.cookies import SimpleCookie

from .request import Request
from .log import logger


class AppRequestContext(object):
    def __init__(self, app, environ):
        self.app = app
        self.environ = environ
        self.env = environ
        self.uri = environ['PATH_INFO'] + environ['QUERY_STRING']
        self.request = Request(environ)
        self._cookies = SimpleCookie()

    @property
    def cookies(self):
        """
        这里是服务器返回客户端的cookies (server -> client)
        如果要获取客户端请求中的cookies，看`Request.cookies`
        """
        return self._cookies

    def get_cookie(self, name):
        return self._cookies.get(name, None)

    def set_cookie(self, name, value, expires=None, domain=None, max_age=None,
                   path='/', secure=None, httponly=None, version=None):
        """创建新cookie或更新已有cookie"""

        old = self._cookies.get(name)
        if old is not None and old.coded_value == '':
            # deleted cookie
            self._cookies.pop(name, None)

        self._cookies[name] = value
        c = self._cookies[name]

        if expires is not None:
            c['expires'] = expires
        elif c.get('expires') == 'Thu, 01 Jan 1970 00:00:00 GMT':
            del c['expires']

        if domain is not None:
            c['domain'] = domain

        if max_age is not None:
            c['max-age'] = str(max_age)
        elif 'max-age' in c:
            del c['max-age']

        c['path'] = path

        if secure is not None:
            c['secure'] = secure
        if httponly is not None:
            c['httponly'] = httponly
        if version is not None:
            c['version'] = version

    def del_cookie(self, name):
        pass

    def load_session(self):
        # load self.request.cookies
        pass

    def save_session(self, response):
        """
        if:
            self.set_cookie(name='a', value=1)
        then:
            v = c.output(header='')     # ' a=1; Path=/'
            v[1:] => 'a=1; Path=/'

        :param response:
        :return:
        """
        if self._cookies:
            for c in self._cookies.values():
                v = c.output(header='')
                logger.debug("cookie value: '{}'".format(v))
                h = ('Set-Cookie', v[1:])
                response.headers.append(h)

