# -*- coding: utf-8 -*-
__author__ = 'sam'

from serial import *

ser = Serial()
ser.port = 3
ser.timeout = 300
if False == ser.isOpen():
    ser.open()

for i in range(0, 5):
    text = ser.read(1)
    if text:
        n = ser.inWaiting()
        if n:
            text = text + ser.read(n)

        print("Received %d bytes" % len(text))

        for recv_bytes in text:
            print("%d  " % (int(recv_bytes.encode("hex"), 16)))

    print "\r\r"


#out_data = '\x0a\x00\x80\x09\x00\x06\x49\x00\x50\x00\x51\x00'
#ser.write(out_data)
ser.close()