#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from django.conf import settings as conf


def settings(request):
    """
        Add settings to the template
    """
    return {'SETTINGS': conf}
