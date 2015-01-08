# -*- coding: utf-8 -*-
__author__ = 'sam'

import socket
import select
import sys
import argparse
import re
import urllib2
from ctypes import *
from serial import *

nxt = None

def init_serial(com):
    ser = Serial()
    ser.port = com
    ser.timeout = 0

    if False == ser.isOpen():
        try:
            ser.open()
        except:
            print("Can not open COM%d" % (com+1))
            return None

    return ser

def nxt_write(msgs):
    msg = str('\x00\x80\x09\x05')
    msg_len = len(msgs) + 1
    total_msg_len = msg_len + 4
    msg += to_bytes([msg_len])

    for move_byte in msgs:
        msg += to_bytes([move_byte])

    msg += '\x00'
    nxt_bt_msg = to_bytes([total_msg_len]) + msg
    print repr(nxt_bt_msg)

    try:
        nxt.write(nxt_bt_msg)
    except:
        pass

def process_nxt_data(rx_data):
    if (rx_data[0] == "3"):
        nxt_write('UAck')
    elif (rx_data[0] == "2"):
        nxt_write('FAck')
    elif (rx_data[0] == "1"):
        nxt_write('DAck')
    elif (rx_data[0] == "0"):
        nxt_write('BAck')
    elif (rx_data[0] == "4"):
        nxt_write('RAck')
    elif (rx_data[0] == "5"):
        nxt_write('LAck')
    elif (rx_data[0] == "6"):
        print "End of scan"
        nxt_write('EAck')

def serial_read(ser):
    text = ser.read(1)
    if text:
        n = ser.inWaiting()
        if n:
            text = text + ser.read(n)

        print text[6:]
        process_nxt_data(text[6:])

if __name__ == "__main__":
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(metavar='N', default = 0, type = int,
                        help = 'The COM port (N) that connected to NXT',
                        dest = 'com')
    args = parser.parse_args()'''

    global nxt
    nxt = init_serial(3)

    try:
        while True:
            if nxt != None:
                serial_read(nxt)
    except KeyboardInterrupt:
        pass