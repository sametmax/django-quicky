#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.http import HttpResponse
from django.conf import settings

__all__ = ['HttpResponseException', 'setting']


class HttpResponseException(HttpResponse, Exception):
    pass


def setting(name, default=None):
    """
        Gets settings from django.conf if exists, returns default value otherwise

        Example:

        DEBUG = setting('DEBUG', False)
    """
    return getattr(settings, name, default)


def get_client_ip(request):
    """
        Return the client IP address as a string.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]

    return request.META.get('REMOTE_ADDR')
