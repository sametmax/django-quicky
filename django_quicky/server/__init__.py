#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from django.core import management
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import AdminMediaHandler

from wsgiserver import CherryPyWSGIServer as Server


def run_server(*args, **kwargs):
    management.call_command('runserver', *args, **kwargs)


def cherrypy_server(host='localhost', port=8000, threads=4,
                    ssl_certificate=None, ssl_private_key=None):

    app = AdminMediaHandler(WSGIHandler())
    server = Server((host, int(port)), app, threads, "django")

    if ssl_certificate and ssl_private_key:
        server.ssl_certificate = ssl_certificate
        server.ssl_private_key = ssl_private_key

    return app, server
