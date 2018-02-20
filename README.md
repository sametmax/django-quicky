Django-quicky
==============

A collection of tools to make setting up Django quicker.

It is NOT a microframework and is meant to be used withing an ordinary Django
setup as it's fully compatible with the standard usages.

You will love this tool if you ever wished you could do:

```python
@url('/user/\d+')
@view(render_to='user.html')
def user_view(request, id):
    # ...
    return {'users': users}


@user_view.ajax(render_to='json')
def ajax_user_view(request, id, context):
    # ...
    return context
```

Note that this software is beta, but it's already used in production.

Just `pip install django-quicky`.


Url decorators
===============

If you like micro frameworks like [bottle](http://bottlepy.org/docs/dev/), you probably miss the very easy way to declare a route.

Now you can do this:

```python
from django_quicky import routing

url, urlpatterns = routing()


@url('/any/regex/django/accepts')
def an_ordinary_view(request):
    #...


@url('/you/can/stack/routing')
@url('/any/regex/django/accepts')
def an_ordinary_view(request):
    # ...
```

Just declare your routes in the view. And use your view file in `URL_ROOT` or any `include()` like you would do with `urls.py`.

**Remember, order matters, so:**

- views declared first will match first. Avoid declaring `@url(r'^$')` first (at the begining of views.py) or it will prevent others from matching.
- when using several `@url` on the same view, the first applied (the lowest `@url` in the decorators pile) will match first.
- always put `@url` as the LAST decorator applied (at the very top of the decorators pile).

If you are in the mood for fancy stuff, and feel like adding a url manually, just do:

```python
urlpatterns.add_url(url, view, [kwargs, name, prefix])
```

And for an include:

```python
urlpatterns.include(url, view, [name, prefix])
```

And since you often add the admin url:

    urlpatterns.add_admin(url)

Adding http error views is neither hard nor useful (most of the time), but for completeness:

```python
@url.http404
def http404(request):
    # ...
```
Of course, your view needs to return the proper status code.


View decorators
===============

Rendering template and json bore you to death?


```python
from django_quicky import view

@view(render_to='template.html')
def an_ordinary_view(request):
    return {'stuff': stuff}


@view(render_to='json')
def a_json_view(request):
    return {'stuff': stuff}


@view(render_to='raw')
def a_raw_view(request):
    return 'hey'
```

For the first one, the returned dictionary will be used as a context (with RequestContext) to render the template. For the second one, it will be serialised to JSON. The last one will just return the string.

**/!\ WARNING:**

The view decorator should always be the first decorator to be applied (the lowest one in the decorator pile).


Conditional rendering
=======================

You can also declare alternatives based on a condition, for a single view:

```python
from django_quicky import view

@view(render_to='template.html')
def common_views(request):
    return {'stuff': stuff}

@common_views.post()
def post_view(request, context):
    # do more stuff
    return context

@common_views.ajax(render_to='json')
def json_view(request, context):
    return context
```

The first view will be rendered as-is if it receives a normal GET request. The second view will be rendered only for POST requests, but will be passed the result of the execution of the first view. The second view will be rendered only for AJAX requests, and as JSON, but will be passed the result of the execution first view.

Just remember that alternative views must accept `context` as a parameter, because they will always receive the result of the main view.

Oh, and of course you can define your own conditions:

```python
@view(render_to='template.html')
def common_views(request):
    return {'stuff': stuff}

@common_views.render_if(conditon=a_function_that_returns_a_bool)
def conditional_view(request, context):
    # do more stuff
    return context
```

Super user middleware
======================

Double authentification? Short session timeout? Permission issue? Loooooooong password.

In, dev, just do:

```python
if DEBUG:

    MIDDLEWARE_CLASSES += (
        'django_quicky.middleware.ForceSuperUserMiddleWare',
    )
```

You will always be logged in as a super user. No password required. No timeout.


Serve static middleware
========================

Serving static files IN DEV without worries:

```python
if DEBUG:

    MIDDLEWARE_CLASSES += (
        'django_quicky.middleware.StaticServe',
    )
```

And if you do want to test your site with `DEBUG` set to False, you can just remove the condition.

The middleware accesses ```request.META['HTTP_HOST']``` on requests but uses "django_quicky_fake_host" as a fallback for clients that don't provide it via headers (e.g: Django's test client). If you want to specify a different fallback host, you can do so by setting ```DJANGO_QUICKY_DEFAULT_HOST``` in your settings.py file.

(Idea borrowed from the excellent [django-annoying](https://bitbucket.org/offline/django-annoying/wiki/Home), but I stripped the internal test on `DEBUG` which is a pain during testing.)


Settings context processor
==========================

Because everyone ends up needing access to the settings in his templates one day or the other:

```python
TEMPLATE_CONTEXT_PROCESSORS = (
    ...
    "django_quicky.context_processors.settings"
)
```

Loading settings
=====================

When you are not in Django, you may still want to import some django pieces, but they require a settings file.

This function make it easy to do so:

```python
from django_quicky import load_config
load_config('/absolute/path/to/setting/file.py')
```

You can also call it with a relative path:

```python
load_config('../../relative/path/to/setting/file.py')
```

But the starting point will be the one given with os.getcwd(), which is probably not what you want. You can force a starting point, most often you'll want the current file, by passing it manually:

```python
load_config('../../relative/path/to/setting/file.py', starting_point=__file__)
```

`starting_point` can be either a file (basename will be stripped) or a directory.

You can also pass a directory path, in which case Python will try to load a settings module from this directory:

```python
load_config('/path/to/settings/directory')
```

It will attempt to load a module named as in `os.environ['DJANGO_SETTINGS_MODULE']` or default to `settings`. You can force the name by passing the `settings_module` parameter.

DEBUGGING
==========

The first rule when debugging decorators, is to be sure you use the right syntax: `@decorator` and `@decorator()` are very different and both syntaxically valid. In django-quickly's case, all decorators should be called with `@decorator()` or `@decorator(arguments)`.

Also remember that when it comes to decorators, **order matters**. Most of the time, you don't care about the order you apply your decorators, but in this case, you should ALWAYS apply `@view` first and `@url` last. E.G:

```python
@url(r'$')
@login_required
@view('app/home.html')
def home(request):
    # ...
```
If you don't do this, some decorators will never be executed as `@view` bypasses decorators applied before it and `@url` bypasses decorators after it.

Also, the order in which you declare your fonction matters, just like patterns order matters in `urls.py`. So avoid putting global matching urls such as `@url('^$')` at the begining of `views.py`, otherwise this view will be used all the time, since the others will never have a chance to match.


Last words
=============

There are other utility functions, but I didn't take the time to document them here, so you'll have to dig in the code. fields.py contains some useful model fields, utils.py has some shortcut functions and models.py comes with tools to get random entries or patch a model.

------------------------------

BTW, it's under the [zlib license](http://www.zlib.net/zlib_license.html).

It embeds [namegen](https://github.com/amnong/namegen), a name generator under BSD license.
