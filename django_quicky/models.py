#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import types

from random import randint


__all__ = ['get_random_objects', 'get_object_or_none', 'patch_model']



def get_random_objects(model=None, queryset=None, count=float('+inf')):
    """
       Get `count` random objects for a model object `model` or from
       a queryset. Returns an iterator that yield one object at a time.

       You model must have an auto increment id for it to work and it should
       be available on the `id` attribute.
    """
    from django.db.models import Max
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


def get_object_or_none(klass, *args, **kwargs):
    """
        Uses get() to return an object or None if the object does not exist.

        klass may be a Model, Manager, or QuerySet object. All other passed
        arguments and keyword arguments are used in the get() query.
    """

    from django.shortcuts import _get_queryset
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None



def patch_model(model_to_patch, class_to_patch_with):
    """
        Adapted from https://gist.github.com/1402045

        Monkey patch a django model with additional or
        replacement fields and methods.

            - All fields and methods that didn't exist previously are added.

            - Existing methods with the same names are renamed with
              <methodname>__overridden, so there are still accessible,
              then the new ones are added.

            - Existing fields with the same name are deleted and replaced with
              the new fields.

        The class used to patch the model MUST be an old-style class (so
        this may not work with Python 3).

        Example (in your models.py):

            from django.contrib.auth.models import User
            from django_quicky.models import patch_model

            class UserOverride: # we don't need to inherit from anything
                email = models.EmailField(_('e-mail address'), unique=True)
                new_field = models.CharField(_('new field'), max_length=10)

                def save(self, *args, **kwargs):

                    # Call original save() method
                    self.save__overridden(*args, **kwargs)

                    # More custom save

            patch_model(User, UserOverride)

    """
    from django.db.models.fields import Field

    # The _meta attribute is where the definition of the fields is stored in
    # django model classes.
    patched_meta = getattr(model_to_patch, '_meta')
    field_lists = (patched_meta.local_fields, patched_meta.local_many_to_many)

    for name, obj in class_to_patch_with.__dict__.iteritems():

        # If the attribute is a field, delete any field with the same name.
        if isinstance(obj, Field):

            for field_list in field_lists:

                match = ((i, f) for i, f in enumerate(field_list) if f.name == name)
                try:
                    i, field = match.next()
                    # The creation_counter is used by django to know in
                    # which order the database columns are declared. We
                    # get it to ensure that when we override a field it
                    # will be declared in the same position as before.
                    obj.creation_counter = field.creation_counter
                    field_list.pop(i)
                finally:
                    break

        # Add "__overridden" to method names if they already exist.
        elif isinstance(obj, (types.FunctionType, property,
                               staticmethod, classmethod)):

            # rename the potential old method
            attr = getattr(model_to_patch, name, None)
            if attr:
                setattr(model_to_patch, name + '__overridden', attr)

            # bind the new method to the object
            if isinstance(obj, types.FunctionType):
                obj = types.UnboundMethodType(obj, None, model_to_patch)

        # Add the new field/method name and object to the model.
        model_to_patch.add_to_class(name, obj)


