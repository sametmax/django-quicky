Django-quicky
==============

A collection of toys to skip the forplay with Django and go straight to the point: url and view decorators.

You will fall in love with it if you ever had the fantasm you could do:

    @url('/user/\d+')
    @view(render_to='user.html'):
    def user_view(request, id)
        ...
        return {'users': users}


    @user_view.ajax(render_to='json')
    def ajax_user_view(request, id, context):
        ...
        return context

And yes, this is alpha software, but you already want it, so don't fight it !

So `pip install django-quicky`.

Url decorators
===============

If you like micro frameworks like <a href="http://bottlepy.org/docs/dev/">bottle</a>, you probably miss the very easy way to declare a route.

Shhh, baby. Talk no more:

    from django_quicky import routing

    url, urlpatterns = routing()


    @url('/any/regex/django/accepts')
    def an_ordinary_view(request):
        ...


    @url('/you/can/stack/routing')
    @url('/any/regex/django/accepts')
    def an_ordinary_view(request):
        ...


Just declare your routing in the view. And use your view file in `URL_ROOT` or any `include()` like you would do with `urls.py`.

**Remember, order matters, so:**

- views declared first will match first. Avoid declaring `@url(r'^$')` first (at the begining of views.py) or it will prevent other from matching.
- when using several `@url` on the same view, the first applied (the lowest `@url` in the decorators pile) will match first.
- always put `@url` as the LAST decorator applied (at the very top of the decorators pile).

If you are in the mood for fancy stuff, like adding an url manually, just do:

    urlpatterns.add_url(url, view, [kwargs, name, prefix])

And for an include:

    urlpatterns.include(url, view, [name, prefix])

And since you often add the admin url:

    urlpatterns.add_admin(url)

Adding http error views is neither hard nor most of the time useful, but for consitency:

    @url.http404
    def http404(request):
        ...

Of course, your view needs to return the proper status code.


View decorators
===============

Rendering template and json bore you to death ? Just say the word:


    from django_quicky import view

    @view(render_to='template.html')
    def an_ordinary_view(request):
        return {'stuff': stuff}


    @view(render_to='json')
    def an_json_view(request):
        return {'stuff': stuff}


For the first one, the returned dictionary will be used as a context to render the template. For the second one, it will be serialised to JSON.

**/!\ WARNING:**

The view decorator should always be the first decorator to be applied (the lowest one in the decorator pile).


Conditional rendering
=======================

Because I know you like dirty talking and big words...

You can also declare alternative rendering:


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

The first view will be rendered as-is if it receives a normal GET request. The second vew will be rendered only for POST requests, but will be passed the result of the first view before. The second vew will be rendered only for AJAX requests, and as JSON, but will be passed the result of the first view before.

Just remember that alternative views must accept `context` as a parameter, because they will always receive the result of the main view.

Oh, and of you can define your own conditions:


    @view(render_to='template.html')
    def common_views(request):
        return {'stuff': stuff}

    @common_views.render_if(conditon=a_function_that_returns_a_bool)
    def conditional_view(request, context):
        # do more stuff
        return context


Super user middleware
======================


Double authentification ? Short session timeout ? Permission issue ? Loooooooong password.

In, dev, just do:

    if DEBUG:

        MIDDLEWARE_CLASSES += (
            'django_quicky.middleware.ForceSuperUserMiddleWare',
        )


You wil always be logged in as a super user. No password required. No timeout.


Serve static middleware
========================


Serving static files in dev without worries:


    if DEBUG:

        MIDDLEWARE_CLASSES += (
            'django_quicky.middleware.StaticServe',
        )

And if you do want to test your site with `DEBUG` set to False, you can just remove the condition.

(Idea borrowed from the excellent <a href="https://bitbucket.org/offline/django-annoying/wiki/Home">django-annoying</a>, but I stripped the internal test on `DEBUG` which is a pain for testing.)

Settings context processor
==========================

Because you always need access to settings in your template one day or the other, but most of the time, right now:

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        "django_quicky.context_processors.settings"
    )


DEBUGGING
==========

The first rule when debugging decorators, is to be sure you use the right syntax: `@decorator` and `@decorator()` are all very different and both valid. In django-quickly case, all decorators should be called with `@decorator()` or `@decorator(arguments)`.

Also remember that when it comes to decorators, **order matters**. Most of the time, you don't care about the order you apply your decorators, but in this case, you should ALWAYS apply `@view` first and `@url` last. E.G:

    url(r'$')
    @login_required
    @view('app/home.html')
    def home(request):
        ...

If you don't do this, some decorators will never be executed as `@view` bypass decorators applied before it and `@url` by pass decorators after it.

Also, the order in which you declare your fonction matters, just like patterns order matter in `urls.py`. So avoid putting global matching urls such as `@url('^$')` at the begining of `views.py`, otherwise this view will be used all the times, since the others will never have a chance to match.

------------------------------

BTW, it's under the <a href="http://www.zlib.net/zlib_license.html">zlib licence</a>.

It embed <a href="https://github.com/amnong/namegen">namegen</a>, a name generator under BSD licence.