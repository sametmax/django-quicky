#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import re

from django.conf import settings
from django.views.static import serve
from django.contrib.staticfiles.views import serve as serve_static

from django.contrib.auth.models import User


class ForceSuperUserMiddleWare(object):
    """
        Developpement middleware forcing login with a super user so you
        don't have to login or worry about access rights.
    """

    def process_request(self, request):

        request.user = User.objects.filter(is_superuser=True)[0]


class StaticServe(object):
    """
        Django middleware for serving static files instead of using urls.py.

        It serves them wether you are set DEBUG or not, so put it into
        a separate settings file to activate it at will.
    """

    media, static = settings.MEDIA_URL.rstrip('/'), settings.STATIC_URL.rstrip('/')
    media_regex = re.compile(r'^%s/(?P<path>.*)$' % media)
    static_regex = re.compile(r'^%s/(?P<path>.*)$' % static)


    def process_request(self, request):

        match = self.media_regex.search(request.path)
        if match:
            return serve(request, match.group(1), settings.MEDIA_ROOT)

        match = self.static_regex.search(request.path)
        if match:
            return serve_static(request, match.group(1), insecure=True)
