# -*- coding: utf-8 -*-

__author__ = 'Gang.Wang'

import sys
import argparse
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

    def get_calibration_info(self):
        return self.wiimote_calibration_x0, \
                self.wiimote_calibration_y0, \
                self.wiimote_calibration_z0, \
                self.wiimote_calibration_xg, \
                self.wiimote_calibration_yg, \
                self.wiimote_calibration_zg

turn_left = 1 << 0
turn_right = 1 << 1
turn_forward = 1 << 0
turn_backward = 1 << 1

def main_process(wii, bt_com):
    while wii.read():
        wii_data = wii.get_read_buffer()
        x0, y0, z0, xg, yg, zg = wii.get_calibration_info()
        #core_button_byte1 = int(wii_data.raw[1].encode("hex"), 16)
        core_button_byte2 = int(wii_data.raw[2].encode("hex"), 16)

        # We only take the data when 'A' button is pressed
        if (core_button_byte2 & BB_BYTE2_A) != BB_BYTE2_A:
            nxt_motor_stop_cmd = create_string_buffer('\x0a\x00\x80\x09\x00\x06', 12)
            try:
                bt_com.write(nxt_motor_stop_cmd)
            except:
                pass

            continue

        raw_x = int(wii_data.raw[3].encode("hex"), 16)
        raw_y = int(wii_data.raw[4].encode("hex"), 16)
        #raw_z = int(wii_data.raw[5].encode("hex"), 16)

        x = float((float(raw_x) - x0) / (float(xg) - x0))
        actual_x = int(x * 100)
        if (actual_x < -100):
            actual_x = -100
        if (actual_x > 100):
            actual_x = 100
        y = float((float(raw_y) - y0) / (float(yg) - y0))
        actual_y = int(y * 100)
        if (actual_y < -100):
            actual_y = -100
        if (actual_y > 100):
            actual_y = 100

        if (actual_x > 0):
            X_BYTE_INT = turn_left
        elif (actual_x < 0):
            X_BYTE_INT = turn_right
        else:
            X_BYTE_INT = 0

        if (actual_y > 0):
            Y_BYTE_INT = turn_forward
        elif (actual_y < 0):
            Y_BYTE_INT = turn_backward
        else:
            Y_BYTE_INT = 0

        direction_int = (X_BYTE_INT << 4) | (Y_BYTE_INT)

        nxt_data_prefix = create_string_buffer('\x0a\x00\x80\x09')
        nxt_motor_data = nxt_data_prefix.raw + '\x06' + \
                    to_bytes([abs(actual_x)]) + '\x00' + \
                    to_bytes([abs(actual_y)]) + '\x00' + \
                    to_bytes([direction_int]) + '\x00'
        print repr(nxt_motor_data)
        try:
            bt_com.write(nxt_motor_data)
        except:
            pass
        print("X:%d Y:%d" % (actual_x, actual_y))
        print("0x%x  " % direction_int)
        #actual_z = float((float(raw_z) - z0) / (float(zg) - z0))


        '''
        print("raw_x:%d raw_x - x0:%d xg - x0:%d" % \
                (raw_x, (raw_x - x0), (xg - x0))),
        print("X: %f %d" % (actual_x, actual_x * 100))

        print("raw_y:%d raw_y - y0:%d yg - y0:%d" % \
                (raw_y, (raw_y - y0), (yg - y0))),
        print("Y: %f %d" % (actual_y, actual_y * 100))

        print("raw_z:%d raw_z - z0:%d zg - z0:%d" % \
                (raw_z, (raw_z - z0), (zg - z0))),
        print("Z: %f %d" % (actual_z, actual_z * 100))
        print

        if core_button_byte1 & BB_BYTE1_DOWN:
            print ("Down")
        elif core_button_byte1 & BB_BYTE1_LEFT:
            print ("Left")
        elif core_button_byte1 & BB_BYTE1_RIGHT:
            print "Right"
        elif core_button_byte1 & BB_BYTE1_UP:
            print "Up"
        '''


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(metavar='N', default = 0, type = int, \
                        help = 'The COM port (N) that connected to NXT', \
                        dest = 'com')
    args = parser.parse_args()

    wii = wiimote()
    ret = wii.open()
    if (0 != ret):
        sys.exit(-1)

    ser = Serial()
    ser.port = (args.com - 1)
    ser.timeout = 300
    if False == ser.isOpen():
        try:
            ser.open()
        except:
            print("Can not open COM%d" % (args.com - 1))
            wii.close()
            sys.exit(-1)

    try:
        main_process(wii, ser)
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