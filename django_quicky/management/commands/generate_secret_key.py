# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding= UTF-8 -*-

"""
    Generate a django secret key. Does not add it to settings.py.
"""


from django.core.management.base import BaseCommand

from django_quicky.utils import generate_secret_key


class Command(BaseCommand):

    help = 'Generates a Django secret key. Does not add it to settings.py.'


    def handle_noargs(self):
        print(generate_secret_key())


if __name__ == '__main__':
    print(generate_secret_key())
