# -*- coding: utf-8 -*-
__author__ = 'sam'

from serial import *

ser = Serial()
ser.port = 3
ser.timeout = 0

try:
    ser.open()
except:
    print("Can not open COM3")

while(1):
    out_data = '\x09\x00\x80\x09\x05\x05\x41\x42\x43\x44\x00'
    ser.write(out_data)
    try:
    #print ("Read %d" % i)
        text = ser.read(1)
        if text:
            n = ser.inWaiting()
            if n:
                text = text + ser.read(n)

            #print("Received %d bytes" % len(text))
            print text[6:]
            '''
            for recv_bytes in text[6:]:
                print('%c'%(int(recv_bytes.encode("hex"), 16))),
                '''

        #print "\n"

    except KeyboardInterrupt:
        print "Quit"
        ser.close()
        sys.exit(0)

#out_data = '\x0a\x00\x80\x09\x00\x06\x49\x00\x50\x00\x51\x00'
#ser.write(out_data)
ser.close()