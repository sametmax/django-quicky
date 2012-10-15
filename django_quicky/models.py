#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

def get_random_objects(model=None, queryset=None, count=float('+inf')):
    """
       Get `count` random objects for a model object `model` or from
       a queryset. Returns an iterator that yield one object at a time.

       You model must have an auto increment id for it to work and it should
       be available on the `id` attribute.
    """

    if not queryset:
        try:
            queryset = model.objects.all()
        except AttributeError:
            raise ValueError("You must provide a model or a queryset")

    max_ = queryset.aggregate(Max('id'))['id__max']
    i = 0
    while i < count:
      try:
          yield queryset.get(pk=randint(1, max_))
          i += 1
      except queryset.model.DoesNotExist:
          pass