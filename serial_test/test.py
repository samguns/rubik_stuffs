# -*- coding: utf-8 -*-
__author__ = 'sam'

from serial import *
import struct

s_data = '\x80\x09\x00\x06\x49\x00\x50\x00\x51\x00'
print("%d %d %d %d" % (int(s_data[0].encode("hex"), 16),
						int(s_data[1].encode("hex"), 16),
						int(s_data[2].encode("hex"), 16),
						int(s_data[3].encode("hex"), 16)))