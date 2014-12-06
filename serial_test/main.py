# -*- coding: utf-8 -*-
__author__ = 'sam'

from serial import *

ser = Serial()
ser.port = 5
ser.timeout = 30
if False == ser.isOpen():
    ser.open()

for i in range(0, 30):
    recv_bytes = ser.read(14)
    print("%d %d %d %d %d %d %d %d %d %d %d %d" % (int(recv_bytes[0].encode("hex"), 16),
                            int(recv_bytes[1].encode("hex"), 16),
                            int(recv_bytes[2].encode("hex"), 16),
                            int(recv_bytes[3].encode("hex"), 16),
                            int(recv_bytes[4].encode("hex"), 16),
                            int(recv_bytes[5].encode("hex"), 16),
                            int(recv_bytes[6].encode("hex"), 16),
                            int(recv_bytes[7].encode("hex"), 16),
                            int(recv_bytes[8].encode("hex"), 16),
                            int(recv_bytes[9].encode("hex"), 16),
                            int(recv_bytes[10].encode("hex"), 16),
                            int(recv_bytes[11].encode("hex"), 16)))

#s_data = '\x80\x09\x00\x06\x49\x00\x50\x00\x51\x00'
#ser.write(s_data)
ser.close()