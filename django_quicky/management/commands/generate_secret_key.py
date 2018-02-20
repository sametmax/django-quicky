# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding= UTF-8 -*-

"""
    Generate a django secret key. Does not add it to settings.py.
"""


from django.core.management.base import BaseCommand

from django_quicky.utils import secret_key


class Command(BaseCommand):

    help = 'Generates a Django secret key. Does not add it to settings.py.'

    def handle(self, *args, **kwargs):
        self.stdout.write(secret_key())

