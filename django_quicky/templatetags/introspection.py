#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

"""
    Tag to use python introspection in a Django template
"""

from django import template
register = template.Library()


@register.filter
def getattr(obj, args):
    """ 
        Try to get an attribute from an object.

        Example: {% if block|getattr:"editable,True" %}

        Beware that the default is always a string, if you want this
        to return False, pass an empty second argument:

        {% if block|getattr:"editable," %}

        Source: http://djangosnippets.org/snippets/38/
    """
    try:
        args = args.split(',')
    except AttributeError:
        raise AttributeError(('"%s" is not a proper value the "getattr" '
                              'filter applied to "%s"') % (args, obj))

    if len(args) == 1:
        (attribute, default) = [args[0], ''] 
    else:
        (attribute, default) = args

    try:
        return obj.__getattribute__(attribute)
    except AttributeError:
         return  obj.__dict__.get(attribute, default)
    except:
        return default