# -*- coding: utf-8 -*-
__author__ = 'sam'

from serial import *
import struct

ser = Serial()
ser.port = 3
ser.timeout = 300
if False == ser.isOpen():
    ser.open()

for i in range(0, 50):
    out_data = '\x0a\x00\x80\x09\x00\x06\x49\x00\x50\x00\x51\x00'
    ser.write(out_data)

ser.close()
