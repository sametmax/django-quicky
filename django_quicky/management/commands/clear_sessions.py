#!/usr/bin/env python
# -*- coding= UTF-8 -*-

"""
    Delete all sessions
"""

from optparse import make_option

from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session


class Command(BaseCommand):

    help = 'Delete all sessions from the server'

    option_list = BaseCommand.option_list + (

        make_option('--no-confirm',
            action='store_true',
            dest='no_confirm',
            default=False,
            help=u"Don't ask for confirmation"),

    )

    def handle(self, *args, **options):

        total = Session.objects.all().count()

        if not options['no_confirm']:
            confirm = raw_input('This will delete all %s sessions. Are you sure ? [y/N]\n' % total)
            if confirm.lower() not in ('y', 'yes'):
                return

        Session.objects.all().delete()
        print '%s sessions deleted' % total
