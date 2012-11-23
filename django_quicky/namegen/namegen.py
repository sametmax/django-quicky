#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Generate random usernames in
"""

import random

from .names import names as default_names


class NameGenerator(object):

    def __init__(self, names=None):
        self.names = names or default_names


    def __call__(self):
        return self.names.pop(random.randrange(len(self.names)))

    def __iter__(self):
        while self.names:
            yield self()
