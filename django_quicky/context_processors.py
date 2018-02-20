#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from django.views.debug import get_safe_settings


class SafeSettings(object):
    """
        Map attributes to values in the safe settings dict
    """
    def __init__(self):
        self._settings = get_safe_settings()

    def __getattr__(self, name):
        try:
            return self._settings[name.upper()]
        except KeyError:
            raise AttributeError


settings_obj = SafeSettings()


def settings(request):
    return {'settings': settings_obj}

