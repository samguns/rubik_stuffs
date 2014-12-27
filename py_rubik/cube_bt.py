# -*- coding: utf-8 -*-
__author__ = 'sam'

import sys
import argparse
from ctypes import *
from serial import *

U = 0
F = 1
D = 2
B = 3
R = 4
L = 5

TURN_180 = 1
COUNTER_CLOCKWISE = 1

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(metavar='N', default = 0, type = int, \
                        help = 'The COM port (N) that connected to NXT', \
                        dest = 'com')
    args = parser.parse_args()

    ser = Serial()
    ser.port = (args.com - 1)
    ser.timeout = 10
    if False == ser.isOpen():
        try:
            ser.open()
        except:
            print("Can not open COM%d" % args.com)
            sys.exit(-1)

    cube_moves = raw_input("Cube move --> ")
    cube_moves.strip()
    cube_moves += 's'
    cube_moves = cube_moves.replace(' ', 's')
    cube_moves = cube_moves.replace('\'', 'n')

    nxt_moves = []
    nxt_byte = 0
    for move in cube_moves:
        print move,
        if move == 'U':
            nxt_byte |= U << 2
        elif move == 'F':
            nxt_byte |= F << 2
        elif move == 'D':
            nxt_byte |= D << 2
        elif move == 'B':
            nxt_byte |= B << 2
        elif move == 'R':
            nxt_byte |= R << 2
        elif move == 'L':
            nxt_byte |= L << 2
        elif move == '2':
            nxt_byte |= TURN_180 << 1
        elif move == 'n':
            nxt_byte |= COUNTER_CLOCKWISE
        elif move == 's':
            nxt_moves.append(nxt_byte)
            nxt_byte = 0
    print ' '
    #print nxt_moves

    msg = str('\x00\x80\x09\x05')
    msg_len = len(nxt_moves) + 1
    total_msg_len = msg_len + 4
    msg += to_bytes([msg_len])

    for move_byte in nxt_moves:
        msg += to_bytes([move_byte])

    msg += '\x00'
    nxt_bt_msg = to_bytes([total_msg_len]) + msg
    print repr(nxt_bt_msg)

    try:
        ser.write(nxt_bt_msg)
    except:
        pass
