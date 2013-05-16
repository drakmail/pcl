#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# WSGI handler for PCL.
import os
import sys
import wsgi
wsgi.multiprocess = True
from wsgiref.simple_server import make_server

import index

def application(environ, responser):
    os.environ["REQUEST_URI"] = str(environ["PATH_INFO"])
    os.environ["REMOTE_ADDR"] = environ["REMOTE_ADDR"]
    os.environ["PCL_SUPPRESS_PRINT_TO_CONSOLE"] = "1"
    os.environ["HTTP_ACCEPT_LANGUAGE"] = environ["HTTP_ACCEPT_LANGUAGE"]
    os.environ["HTTP_USER_AGENT"] = environ["HTTP_USER_AGENT"]
    os.environ["PCL_IN_WSGI_MODE"] = "1"
    if "HTTP_COOKIE" in environ:
        os.environ["HTTP_COOKIE"] = environ["HTTP_COOKIE"]

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    os.environ["wsgi.input"] = environ["wsgi.input"].read(request_body_size).decode("utf-8")

    #response_body = ['%s: %s' % (key, value)
    #                for key, value in sorted(environ.items())]
    #response_body = '\n'.join(response_body)

    pcl_main = index.PCL()
    response_body = pcl_main.get_response()

    status = '200 OK'
    response_headers = [("Content-Type", "text/html; charset=utf-8"),
                        ("Content-Length", str(len(response_body)))]

    responser(status, response_headers)

    return [response_body.encode("utf-8")]

httpd = make_server('localhost', 8051, application)
httpd.serve_forever()