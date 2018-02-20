# -*- coding: utf-8 -*-

"""
    Delete migrations
"""

import os
import re
import glob

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.apps import apps
from django.core.management import call_command


class Command(BaseCommand):

    help = 'Delete numered migrations, all tables, then makemigrations and migrate'

    def add_arguments(self, parser):
        parser.add_argument('apps', nargs='*')

    def handle(self, *args, **options):
        own_apps = set(getattr(settings, 'OWN_APPS', []))
        if not own_apps:
            raise CommandError(
                "You need to put a list of your own apps in settings.OWN_APPS"
            )

        installed_apps = set(settings.INSTALLED_APPS)

        bad_apps = ", ".join(own_apps.difference(installed_apps))
        if bad_apps:
            raise CommandError((
                "All apps in settings.OWN_APPS must be in "
                "settings.INSTALLED_APPS. Those are not: {}"
            ).format(bad_apps))

        selected_apps = set(options['apps'] or own_apps)

        bad_apps = ", ".join(selected_apps.difference(own_apps))
        if bad_apps:
            raise CommandError((
                "All apps passed in parameters must be in settings.OWN_APPS. "
                "Those are not: {}"
            ).format(bad_apps))

        apps_list = [a for n, a in apps.app_configs.items() if a.name in selected_apps]

        for app in apps_list:

            for model in app.get_models():
                model.objects.raw(
                    'DROP TABLE {}'.format( model._meta.db_table)
                )

            migrations_files = os.path.join(app.path, 'migrations', '*.py')
            for f in glob.glob(migrations_files):
                if re.match(r'\d\d\d\d', os.path.basename(f)):
                    self.stdout.write("Deleting " + f)
                    os.remove(f)

        for app in apps_list:
                call_command('makemigrations', app.label)

        for app in apps_list:
            call_command('migrate', app.label)

        for app in apps_list:
            migrations_files = os.path.join(app.path, 'fixtures', '*.json')
            for f in glob.glob(migrations_files):
                self.stdout.write("Loading " + f)
                call_command('loaddata', f)

