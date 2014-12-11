# -*- coding: utf-8 -*-
__author__ = 'sam'

from serial import *
from ctypes import *

#out_data = '\x0a\x00\x80\x09\x00\x06\x49\x00\x50\x00\x51\x00'

nxt_motor_prefix = create_string_buffer('\x0a\x00\x80\x09')
actual_x = 20
actual_y = 30
direction_int = 0x22
nxt_motor_data = nxt_motor_prefix.raw + '\x06' + \
                 to_bytes([abs(actual_x)])
'''
nxt_motor_data.raw[6] = chr(abs(actual_x))
nxt_motor_data.raw[7] = '\x00'
nxt_motor_data.raw[8] = chr(abs(actual_x))
nxt_motor_data.raw[9] = '\x00'
nxt_motor_data.raw[10] = chr(direction_int)
nxt_motor_data.raw[11] = '\x00'
'''

print repr(nxt_motor_data)
print nxt_motor_data
print to_bytes([64])