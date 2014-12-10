# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import with_statement
#from __future__ import print_function

__author__ = 'Gang.Wang'

import sys
from ctypes import *
from serial import *

hid_lib = cdll.LoadLibrary('./hidapi.dll')

battery_empty_flag = 1 << 0
extention_flag = 1 << 1

BB_BYTE1_LEFT = 1 << 0
BB_BYTE1_RIGHT = 1 << 1
BB_BYTE1_DOWN = 1 << 2
BB_BYTE1_UP = 1 << 3
BB_BYTE1_PLUS = 1 << 4

BB_BYTE2_TWO = 1 << 0
BB_BYTE2_ONE = 1 << 1
BB_BYTE2_B = 1 << 2
BB_BYTE2_A = 1 << 3
BB_BYTE2_MINUS = 1 << 4
BB_BYTE2_HOME = 1 << 7

class wiimote:
    def __init__(self):
        self.vendor_id = 0x057e
        self.product_id = 0x0306
        self.dev = 0
        self.buffer = create_string_buffer('\000' * 22)
        self.nunchuck_avail = 0

    def close(self):
        if (0 != self.dev):
            print "Bye bye"
            hid_lib.hid_close(self.dev)

    def init_extension(self):
        # The new way to initialize the extension
        # is by writing 0x55 to 0x(4)A400F0, then
        # writing 0x00 to 0x(4)A400FB
        extention_init1 = create_string_buffer('\x16\x04\xa4\x00\xf0\x00\x01\x55', 22)
        hid_lib.hid_write_report(self.dev, byref(extention_init1), 22)

        extention_init2 = create_string_buffer('\x16\x04\xa4\x00\xfb\x00\x01\x00', 22)
        hid_lib.hid_write_report(self.dev, byref(extention_init2), 22)

        # Once initialized, the last six bytes of the register block
        # identify the connected Extension Controller.
        # A six-byte read of register 0xa400fa will return these bytes.
        extention_type = create_string_buffer('\x17\x04\xa4\x00\xfa\x00\x06', 22)
        hid_lib.hid_write_report(self.dev, byref(extention_type), 22)
        self.read()
        if (int(self.buffer.raw[0].encode("hex"), 16) != 0x21):
            self.read()

        print "Read Extention Type:"
        for r_read in self.buffer:
            print("0x%2.2x" % int(r_read.encode("hex"), 16)),
        print

    def read_calibration(self):
        read_cmd = create_string_buffer('\x17\x00\x00\x00\x16\x00\x07', 22)
        hid_lib.hid_write_report(self.dev, byref(read_cmd), 22)
        self.read()
        if (int(self.buffer.raw[0].encode("hex"), 16) != 0x21):
            self.read()

        print "Read Calibration:"
        for r_read in self.buffer:
            print("0x%2.2x" % int(r_read.encode("hex"), 16)),
        print

        self.wiimote_calibration_x0 = \
                    int(self.buffer.raw[6].encode("hex"), 16)
        self.wiimote_calibration_y0 = \
                    int(self.buffer.raw[7].encode("hex"), 16)
        self.wiimote_calibration_z0 = \
                    int(self.buffer.raw[8].encode("hex"), 16)
        self.wiimote_calibration_xg = \
                    int(self.buffer.raw[9].encode("hex"), 16)
        self.wiimote_calibration_yg = \
                    int(self.buffer.raw[10].encode("hex"), 16)
        self.wiimote_calibration_zg = \
                    int(self.buffer.raw[11].encode("hex"), 16)

    def get_status_report(self):
        self.buffer.value = '\x15\x00'
        hid_lib.hid_write_report(self.dev, byref(self.buffer), 2)
        ret = self.read()
        if (ret < 0):
            return

        if (int(self.buffer.raw[0].encode("hex"), 16) != 0x20):
            ret = self.read()
            if (ret < 0):
                return

        print "Status Report:",
        for status_report in self.buffer:
            print("0x%2.2x" % int(status_report.encode("hex"), 16)),
        print

        LF = int(self.buffer.raw[3].encode("hex"), 16)
        VV = int(self.buffer.raw[6].encode("hex"), 16)
        if (LF & battery_empty_flag):
            print "Battery is nearly empty %d" % VV

        if (LF & extention_flag):
            self.init_extension()

        return

    def open(self):
        hid_lib.hid_init()
        dev = hid_lib.hid_open(self.vendor_id, self.product_id, c_void_p())
        if (0 == dev):
            print "Can not find a valid Wii Remote"
            return -1

        hid_lib.hid_set_nonblocking(dev, 1)
        self.dev = dev

        self.read_calibration()
        self.get_status_report()

        # Set LED
        player_LEDs = create_string_buffer('\x11\x10')
        hid_lib.hid_write_report(self.dev, byref(player_LEDs), 2)
        report_mode = create_string_buffer('\x12\x00\x31')
        hid_lib.hid_write_report(self.dev, byref(report_mode), 3)
        ret = self.read()
        if (ret < 0):
            return -2

        return 0

    def read(self):
        if (0 == self.dev):
            return -1

        memset(self.buffer, 0, 22)
        #res = hid_lib.hid_read(self.dev, byref(self.buffer), len(self.buffer))
        res = 0
        while (res == 0):
            res = hid_lib.hid_read(self.dev, byref(self.buffer), len(self.buffer))
            if (res < 0):
                print "Unable to read"
                return -1

        # return number of bytes we've got
        return res

    def get_read_buffer(self):
        return self.buffer

nxt_data_prefix = '\x0a\x00\x80\x09\x00\x06'
def main_process(wii):
    while  wii.read():
        wii_data = wii.get_read_buffer()
        core_button_byte1 = int(wii_data.raw[1].encode("hex"), 16)
        #core_button_byte2 = int(wii_data.raw[2].encode("hex"), 16)
        if core_button_byte1 & BB_BYTE1_DOWN:
            print ("Down")
        elif core_button_byte1 & BB_BYTE1_LEFT:
            print ("Left")
        elif core_button_byte1 & BB_BYTE1_RIGHT:
            print "Right"
        elif core_button_byte1 & BB_BYTE1_UP:
            print "Up"


if __name__ == "__main__":
    wii = wiimote()
    ret = wii.open()
    if (0 != ret):
        sys.exit(-1)

    ser = Serial()
    ser.port = 3
    ser.timeout = 300
    if False == ser.isOpen():
        try:
            ser.open()
        except:
            print "No COM4"
            #wii.close()
            #sys.exit(-1)

    try:
        main_process(wii)
    except KeyboardInterrupt:
        print "Quit"

    ser.close()
    wii.close()

'''
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
'''