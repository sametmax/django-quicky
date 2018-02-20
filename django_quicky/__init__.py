#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import absolute_import


import django

VERSION = __version__ = "0.7"

from .decorators import view, routing
from .utils import setting, load_config
from .models import get_object_or_none
from .deploy import secret_key_from_file