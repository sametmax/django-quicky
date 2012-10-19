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

from namegen.namegen import NameGenerator

from utils import setting


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


