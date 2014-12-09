# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import with_statement

__author__ = 'Gang.Wang'

from ctypes import cdll

hid_lib = cdll.LoadLibrary('./hidapi.dll')

hid_lib.hid_exit()
