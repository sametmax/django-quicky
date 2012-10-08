#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from django.contrib.auth.models import User


class ForceSuperUserMiddleWare(object):
    """
        Developpement middleware forcing login with a super user so you
        don't have to login or worry about access rights.
    """

    def process_request(self, request):

        request.user = User.objects.filter(is_superuser=True)[0]
