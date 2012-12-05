#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.http import HttpResponse
from django.conf import settings

__all__ = ['HttpResponseException', 'setting']


class HttpResponseException(HttpResponse, Exception):
    pass


def setting(name, default):
    """
        Gets settings from django.conf if exists, returns default value otherwise

        Example:

        DEBUG = setting('DEBUG', False)
    """
    return getattr(settings, name, default)


