#!/usr/bin/env python3

import logging
import sys
import urllib
import threading
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

from wsgiref.simple_server import ServerHandler

logging.basicConfig(level=logging.DEBUG)


__version__ = "0.2"


#
# HTTP服务器
#

class WSGIRequestHandler(BaseHTTPRequestHandler):

    server_version = "WSGIServer/" + __version__

    def get_environ(self):
        env = {
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": 'http',
            "wsgi.input": self.rfile,
            "wsgi.errors": sys.stderr,
            "wsgi.multithread": self.server.multithread,
            "wsgi.run_once": False,

            "GATEWAY_INTERFACE": 'CGI/1.1',
            "SERVER_SOFTWARE": self.server_version,

            "SERVER_NAME": self.server.server_address[0],
            "SERVER_HOST": self.server.server_name,
            "SERVER_PORT": str(self.server.server_address[1]),
            "SERVER_PROTOCOL": self.request_version,

            "REMOTE_HOST": self.address_string(),
            "REMOTE_ADDR": self.address_string(),
            "REMOTE_PORT": self.client_address[1],

            "SCRIPT_NAME": '',
            "REQUEST_METHOD": self.command,
        }

        if '?' in self.path:
            path, query = self.path.split('?', 1)
        else:
            path,query = self.path,''

        env['PATH_INFO'] = urllib.parse.unquote(path, 'iso-8859-1')
        env['QUERY_STRING'] = query

        host = self.address_string()
        if host != self.client_address[0]:
            env['REMOTE_HOST'] = host

        if self.headers.get('content-type') is None:
            env['CONTENT_TYPE'] = self.headers.get_content_type()
        else:
            env['CONTENT_TYPE'] = self.headers['content-type']

        length = self.headers.get('content-length')
        if length:
            env['CONTENT_LENGTH'] = length

        for k, v in self.headers.items():
            k = k.replace('-', '_').upper()
            v = v.strip()
            if k in env:
                continue                    # skip content length, type,etc.
            if 'HTTP_'+k in env:
                env['HTTP_'+k] += ','+v     # comma-separate multiple headers
            else:
                env['HTTP_'+k] = v
        return env

    def get_stderr(self):
        return sys.stderr

    def handle(self):
        """Handle a single HTTP request"""
        self.raw_requestline = self.rfile.readline(65537)
        if len(self.raw_requestline) > 65536:
            self.requestline = ''
            self.request_version = ''
            self.command = ''
            self.send_error(414)
            return

        if not self.parse_request():
            # An error code has been sent, just exit
            return

        handler = ServerHandler(
            self.rfile, self.wfile, self.get_stderr(), self.get_environ()
        )
        handler.request_handler = self      # backpointer for logging
        handler.run(self.server.app)


class __WSGIRequestHandler(BaseHTTPRequestHandler, object):
    pass


class BaseWSGIServer(HTTPServer, object):
    multithread = False

    def __init__(self, host, port, app, handler=None):
        if handler is None:
            handler = WSGIRequestHandler

        server_address = (host, int(port))
        HTTPServer.__init__(self, server_address, handler)

        self.app = app

    def serve_forever(self):
        try:
            HTTPServer.serve_forever(self)
        except KeyboardInterrupt:
            pass
        finally:
            self.server_close()


class ThreadedWSGIServer(ThreadingMixIn, BaseWSGIServer):
    multithread = True
    daemon_threads = True


def make_server(host=None, port=None, app=None, threaded=False,
                request_handler=None):
    if threaded:
        return ThreadedWSGIServer(host, port, app, handler=request_handler)
    else:
        return BaseWSGIServer(host, port, app, handler=request_handler)


def run_simple(host, port, app, threaded=False, request_handler=None):
    srv = make_server(host, port, app, threaded, request_handler)
    quit_msg = "(Press CTRL+C to quit)"
    s = f"Running on http://{host}:{port}/ {quit_msg}"
    # print(s)
    logging.info(s)
    # logging.info(f"Running on http://{host}:{port}/ {quit_msg}")
    srv.serve_forever()

#
# 框架
#


context = ctx = threading.local()

_url_map = {
    # rule: view class
}


class Response(object):
    pass


class Yonder(object):
    def __init__(self):
        pass

    def run(self, host='localhost', port=8000, **options):
        options.setdefault('threaded', True)
        return run_simple(host, port, self, **options)

    def dispatch_request(self):
        pass

    def make_response(self):
        pass

    def _load_context(self, environ):
        ctx.env = environ
        ctx.environ = environ
        print(ctx.env)

    def wsgi_app(self, environ, start_response):
        self._load_context(environ)
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'<h1>Hello, web!</h1>']

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


class TestView(object):
    def get(self, ctx):
        pass


def _test():
    app = Yonder()
    host = '0.0.0.0'
    port = 6070
    app.run(host=host, port=port)


if __name__ == "__main__":
    _test()
