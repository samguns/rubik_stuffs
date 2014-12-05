# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import with_statement

__author__ = 'Gang.Wang'

import os, sys
import bluetooth

#nearby_devices = bluetooth.discover_devices()

#for bd_addr in nearby_devices:
    #print "%s  %s" % (bd_addr, bluetooth.lookup_name(bd_addr))

devices = bluetooth.find_service(name = "Nintendo RVL-CNT-01")

for service_providers in devices:
    print service_providers
