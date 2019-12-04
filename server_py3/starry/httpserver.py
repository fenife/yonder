#!/usr/bin/env python3

import time
import sys
from urllib.parse import unquote
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler

from platform import python_implementation
# from wsgiref.simple_server import ServerHandler
from wsgiref.simple_server import SimpleHandler

# logging.basicConfig(level=logging.DEBUG)
from .log import logger


__version__ = "0.2"


#
# HTTP服务器
#


server_version = "WSGIServer/" + __version__
sys_version = python_implementation() + "/" + sys.version.split()[0]
software_version = server_version + ' ' + sys_version


class ServerHandler(SimpleHandler):
    """from wsgiref.simple_server of python lib"""

    server_software = software_version

    def close(self):
        try:
            self.request_handler.log_request(
                self.status.split(' ',1)[0], self.bytes_sent
            )
        finally:
            SimpleHandler.close(self)


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
            path, query = self.path, ''

        env['PATH_INFO'] = unquote(path, 'iso-8859-1')
        env['QUERY_STRING'] = unquote(query)

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

    def log_date_time_string(self):
        """Return the current time formatted for logging."""
        now = time.time()
        year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
        s = "%04d-%02d-%02d %02d:%02d:%02d" % (year, month, day, hh, mm, ss)
        return s

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


def run_simple(host, port, app, threaded=False, request_handler=None, **options):
    srv = make_server(host, port, app, threaded, request_handler)
    quit_msg = "(Press CTRL+C to quit)"
    s = f"Running on http://{host}:{port}/ {quit_msg}"
    # print(s)
    logger.info(s)
    # logging.info(f"Running on http://{host}:{port}/ {quit_msg}")
    srv.serve_forever()


