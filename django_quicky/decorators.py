#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


import json
import types
from functools import wraps, partial

import django
from django.http import HttpResponse
from django.conf.urls import include, url as addurl
from django.shortcuts import render

from .utils import HttpResponseException


__all__ = ["view", "routing"]


def render_if(self, render_to=None, condition=lambda: False):
    """
        Render this view instead of the previous

        This function meant to be bound as a method to any fonction decorated
        with func_name.render_if, func_name being a function you just
        defined before, and decorated with @view.

        @view(render_to='template')
        def my_view(request):
            ...
            return context

        @my_view.render_if(condition=lambda r: r. user.is_authenticated())
        def my_conditional_view(request, context):
            ...

        my_view will always be executed, and should return a dictionary. if
        the user is authenticated, my_conditional_view is called, get the
        dictionary as a context, and should return a dictionary. If not,
        the context returned from my_view will be used directly.

        In any case, the context is rendered to the render_to template.

    """
    def decorator(func):
        self.conditional_calls.append((condition, func, render_to))
        return func
    return decorator

# Thers
render_if_ajax = partial(render_if, condition=lambda r, *a, **k: r.is_ajax())
render_if_get = partial(render_if, condition=lambda r, *a, **k: r.method == 'GET')
render_if_post = partial(render_if, condition=lambda r, *a, **k: r.method == 'POST')


def view(render_to=None, *args, **kwargs):
    """
        Decorate a view to allow it to return only a dictionary and be rendered
        to either a template or json.

        @view(render_to="template"):
        def my_view(request):
            ...
            return {....}

        The returned dict will be used as a context, and rendered with
        the given template and RequestContext as an instance.

        @view(render_to="json"):
        def my_view(request):
            ...
            return {....}

        The returned dict will be used as a context, and rendered as json.

        The view will also gain new attributes that you can use as
        decorators to declare alternative function to execute after the view:

        @view(render_to='user.html'):
        def user_view(request, id)
            ...
            return {'users': users}


        @user_view.ajax(render_to='json')
        def ajax_user_view(request, id, context):
            ...
            return context

        ajax_user_view will be called only if it's an ajax request. It will
        be passed the result of user_view as a context, and it should return
        a dictionary which will be rendered as json.
    """

    decorator_args = args
    decorator_kwargs = kwargs

    def decorator(func):

        func.conditional_calls = []

        func.ajax = types.MethodType(render_if_ajax, func)
        func.get = types.MethodType(render_if_get, func)
        func.post = types.MethodType(render_if_post, func)
        func.render_if = types.MethodType(render_if, func)

        @wraps(func)
        def wrapper(request, *args, **kwargs):
            try:
                for test, view, rendering in func.conditional_calls:
                    if test(request, *args, **kwargs):
                        response = view(request,
                                         context=func(request, *args, **kwargs),
                                        *args, **kwargs)
                        break

                else:
                    response, rendering = func(request, *args, **kwargs), render_to

                rendering = rendering or render_to

                if rendering and not isinstance(response, HttpResponse):

                    if rendering == 'json':
                        if django.VERSION[0] >= 1 and django.VERSION[1] >= 7:
                            return HttpResponse(json.dumps(response),
                                                content_type="application/json",
                                                *decorator_args, **decorator_kwargs)
                        else:
                            return HttpResponse(json.dumps(response),
                                                mimetype="application/json",
                                                *decorator_args, **decorator_kwargs)
                    if rendering == 'raw':
                        return HttpResponse(response,
                                            *decorator_args, **decorator_kwargs)

                    return render(request, rendering, response,
                                  *decorator_args, **decorator_kwargs)


                return response
            except HttpResponseException as e:
                return e

        return wrapper

    return decorator


def routing(root=""):
    """
        Return a url patterns list that Django can use for routing, and
        a url decorator that adds any view as a route to this list.


        url, urlpatterns = routing()

        @url(r'/home/')
        def view(request):
            ...

        @url(r'/thing/(?P<pk>\d+)/$', name="thingy")
        def other_view(request, pk):
            ...

    """

    urlpatterns = UrlList()

    def url(regex, kwargs=None, name=None, prefix=''):

        def decorator(func):

            urlpatterns.append(
                addurl(regex, func, kwargs, name or func.__name__, prefix),
            )

            return func

        return decorator

    def http403(func):
        django.conf.urls.handler403 = func
        return func
    url.http403 = http403

    def http404(func):
        django.conf.urls.handler404 = func
        return func
    url.http404 = http404

    def http405(func):
        django.conf.urls.handler405 = func
        return func
    url.http405 = http405

    return url, urlpatterns


class UrlList(list):
    """
        Sublass list to allow shortcuts to add urls to this pattern.
    """

    admin_added = False


    def add_url(self, regex, func, kwargs=None, name="", prefix=""):
        self.append(addurl(regex, func, kwargs, name, prefix))


    def include(self, regex, module, name="", prefix=""):
        self.add_url(regex, include(module), name=name, prefix=prefix)


    def add_admin(self, url):

        from django.contrib import admin

        if not UrlList.admin_added:
            admin.autodiscover()

        self.include(url, admin.site.urls, 'admin')

        UrlList.admin_added = True
