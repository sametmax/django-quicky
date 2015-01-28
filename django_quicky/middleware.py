#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import re
import random

from django.conf import settings
from django.views.static import serve
from django.contrib.staticfiles.views import serve as serve_static
from django.shortcuts import redirect, render

from django.contrib.auth.models import User

from .namegen.namegen import NameGenerator

from .utils import setting


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

    # STATIC_URL must be defined at least
    static_url = settings.STATIC_URL.rstrip('/')

    # try to get MEDIA_URL
    media_url = setting('MEDIA_URL', '').rstrip('/')

    # try to get MEDIA_URL
    admin_url = setting('ADMIN_MEDIA_PREFIX', '').rstrip('/')

    media_regex = re.compile(r'^%s/(?P<path>.*)$' % media_url)
    static_regex = re.compile(r'^%s/(?P<path>.*)$' % static_url)
    admin_regex = re.compile(r'^%s/(?P<path>.*)$' % admin_url)

    # IF not MEDIA_ROOT is defined, we supposed it's the same as the
    # STATIC_ROOT
    MEDIA_ROOT = setting('MEDIA_ROOT') or setting('STATIC_ROOT')
    ADMIN_ROOT = setting('ADMIN_MEDIA_PREFIX') or setting('STATIC_ROOT')


    def process_request(self, request):

        protocol = 'http' + ('', 's')[request.is_secure()]
        host = request.META.get('HTTP_HOST', setting(
            'DJANGO_QUICKY_DEFAULT_HOST', 'django_quicky_fake_host'))
        prefix = protocol + '://' + host
        abspath = prefix + request.path

        if self.media_url:
            path = abspath if prefix in self.media_url else request.path
            match = self.media_regex.search(path)
            if match:
                return serve(request, match.group(1), self.MEDIA_ROOT)

        if self.admin_url:
            path = abspath if prefix in self.admin_url else request.path
            match = self.admin_regex.search(path)
            if match:
                return serve(request, match.group(1), self.ADMIN_ROOT)

        path = abspath if prefix in self.static_url else request.path
        match = self.static_regex.search(path)
        if match:
            return serve_static(request, match.group(1), insecure=True)


class AutoLogNewUser(object):


    CALLBACK = setting('AUTOLOGNEWUSER_CALLBAK', None)


    def process_request(self, request):


        if 'django-quicky-test-cookie' in request.path:

            if not request.session.test_cookie_worked():
                return render(request, 'django_quicky/no_cookies.html',
                              {'next': request.GET.get('next', '/')})

            request.session.delete_test_cookie()

            first_name = iter(NameGenerator()).next().title()
            username = "%s%s" % (first_name, random.randint(10, 100))
            user = User.objects.create(username=username,
                                       first_name=first_name)
            request.session['django-quicky:user_id'] = user.pk
            next = request.GET.get('next', '/')
            if self.CALLBACK:
                res = self.CALLBACK(request)
            return redirect(res or next)

        if not request.user.is_authenticated():

            user_id = request.session.get('django-quicky:user_id', None)

            if not user_id:

                request.session.set_test_cookie()
                return redirect('/django-quicky-test-cookie/?next=%s' % request.path)

            request.user = User.objects.get(pk=user_id)


