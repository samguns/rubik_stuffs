# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import with_statement
#from __future__ import print_function

__author__ = 'Gang.Wang'

import sys
from ctypes import *

hid_lib = cdll.LoadLibrary('./hidapi.dll')

null_p = c_void_p()
buf = create_unicode_buffer('\000' * 255)
hid_data = create_string_buffer('\000' * 22)

#hid_dev = c_void_p()
hid_dev = hid_lib.hid_open(0x057e, 0x0306, null_p)
if hid_dev == 0:
    sys.exit(0)

hid_lib.hid_get_manufacturer_string(hid_dev, byref(buf), 256)
print(repr(buf.value))
hid_lib.hid_get_product_string(hid_dev, pointer(buf), 256)
print(buf.value)

hid_lib.hid_set_nonblocking(hid_dev, 1)
hid_lib.hid_read(hid_dev, byref(hid_data), 17)

hid_data.value = '\x11\x20'
hid_lib.hid_write_report(hid_dev, byref(hid_data), 2)

hid_data.value = '\x15\x00'
hid_lib.hid_write_report(hid_dev, byref(hid_data), 2)

memset(hid_data, 0, 22)
res = 0
while (res == 0):
    res = hid_lib.hid_read(hid_dev, byref(hid_data), len(hid_data))
    if (res < 0):
        print("Unable to read")

for result in hid_data:
    print("0x%2.2x" % int(result.encode("hex"), 16)),
print

if (int(hid_data.raw[3].encode("hex"), 16) & 0x02):
    print("We have a Extention controller")

hid_lib.hid_close(hid_dev)
hid_lib.hid_exit()
