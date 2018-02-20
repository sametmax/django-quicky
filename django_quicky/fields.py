#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


"""
    Part of the code is borrowed from django-annoying.

    https://bitbucket.org/offline/django-annoying/wiki/Home
"""

from django.db import models

from django.db.models import OneToOneField
from django.db.models.fields.related import SingleRelatedObjectDescriptor

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    add_introspection_rules = lambda x: x


class AutoSingleRelatedObjectDescriptor(SingleRelatedObjectDescriptor):
    def __get__(self, instance, instance_type=None):
        try:
            return super(AutoSingleRelatedObjectDescriptor, self).__get__(instance, instance_type)
        except self.related.model.DoesNotExist:
            obj = self.related.model(**{self.related.field.name: instance})
            obj.save()
            return obj


class AutoOneToOneField(OneToOneField):
    '''
        OneToOneField creates related object on first call if it doesnt exists yet.
        Use it instead of original OneToOne field.

        example:
        class MyProfile(models.Model):
        user = AutoOneToOneField(User, primary_key=True)
        home_page = models.URLField(max_length=255)
        icq = models.CharField(max_length=255)
    '''
    def contribute_to_related_class(self, cls, related):
        setattr(cls, related.get_accessor_name(), AutoSingleRelatedObjectDescriptor(related))



class IntegerRangeField(models.IntegerField):

    """
        Equvalent of the django Integer Field but with min and max value.
    """

    def __init__(self, verbose_name=None, name=None,
                 min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)


    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)



# if South is installed, provide introspection rules for it's migration
# see: http://south.aeracode.org/docs/tutorial/part4.html#tutorial-part-4
add_introspection_rules([
    (
        [IntegerRangeField],
        [],
        {
            "min_value": ["min_value", {"default": None}],
            "max_value": ["max_value", {"default": None}],
        },
    ),
], ["^libs\.models\.IntegerRangeField"])
