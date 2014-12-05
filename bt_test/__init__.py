# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import with_statement

__author__ = 'Gang.Wang'

import os, sys
from bluetooth import *

nearby_devices = discover_devices()

for bd_addr in nearby_devices:
    print "%s - %s" % (lookup_name(bd_addr), bd_addr)

devices = find_service()
for providers in devices:
    print providers
