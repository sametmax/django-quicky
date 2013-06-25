#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


VERSION = __version__ = "0.6"

from decorators import view, routing
from utils import setting, load_config
from models import get_object_or_none

