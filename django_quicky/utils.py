#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import _get_queryset

__all__ = ['HttpResponseException', 'get_object_or_None', 'setting']


class HttpResponseException(HttpResponse, Exception):
    pass


def get_object_or_None(klass, *args, **kwargs):
    """
        Uses get() to return an object or None if the object does not exist.

        klass may be a Model, Manager, or QuerySet object. All other passed
        arguments and keyword arguments are used in the get() query.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def setting(name, default):
    """
        Gets settings from django.conf if exists, returns default value otherwise

        Example:

        DEBUG = setting('DEBUG', False)
    """
    return getattr(settings, name, default)


