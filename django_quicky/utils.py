#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


import imp
import os
import sys

from django.http import HttpResponse
from django.core.management import setup_environ


__all__ = ['HttpResponseException', 'setting', 'get_client_ip', 'load_config']


class HttpResponseException(HttpResponse, Exception):
    pass


def setting(name, default=None):
    """
        Gets settings from django.conf if exists, returns default value otherwise

        Example:

        DEBUG = setting('DEBUG', False)
    """
    from django.conf import settings
    return getattr(settings, name, default)


def get_client_ip(request):
    """
        Return the client IP address as a string.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]

    return request.META.get('REMOTE_ADDR')


def load_config(path, starting_point='.', settings_module='settings'):
    """
        Add the settings directory to the sys.path, import the settings and
        configure django with it.

        You can path an absolute or a relative path to it.

        If you choose to use a relative path, it will be relative to
        `starting_point` by default, which is set to '.'.

        You may want to set it to something like __file__ (the basename will
        be stripped, and the current file's parent directory will be used
        as a starting point, which is probably what you expect in the
        first place).

        :example:

        >>> load_config('../../settings.py', __file__)
    """

    if not os.path.isabs(path):

        if os.path.isfile(starting_point):
            starting_point = os.path.dirname(starting_point)

        path = os.path.join(starting_point, path)

    path = os.path.realpath(os.path.expandvars(os.path.expanduser(path)))

    if os.path.isfile(path):
        module = os.path.splitext(os.path.basename(path))[0]
        path = os.path.dirname(path)
    else:
        module = os.path.environ.get('DJANGO_SETTINGS_MODULE', settings_module)

    sys.path.append(path)

    f, filename, desc = imp.find_module(module, [path])
    project = imp.load_module(module, f, filename, desc)
    setup_environ(project)
