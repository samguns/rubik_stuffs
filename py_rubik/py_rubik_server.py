# -*- coding: utf-8 -*-

__author__ = 'Gang.Wang'

import socket
import select
import sys
import argparse

from serial import *

def serial_read(ser):
    text = ser.read(1)
    if text:
        n = ser.inWaiting()
        if n:
            text = text + ser.read(n)

        print text[6:]


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

readfds = []
android = None
temp = None

def process_data(fd, data):
    global android
    global temp
    if (fd != android):
        if (data == "U"):
            android.sendall("scan\n")
    else:
        temp.sendall("ack\n")

def client_read(fd):
    global readfds
    global android
    data = fd.recv(1024)
    if not data:
        print "Close sock", fd
        fd.close()
        readfds.remove(fd)
        return
    else:
        print data
        if (data == "Android"):
            android = fd
            print "This is an android", android
            return

        process_data(fd, data)

    return

def server_accept(server):
    global readfds
    global temp
    client, address = server.accept()
    print "Connected by", address, client
    readfds.append(client)
    temp = client

def init_server():
    global readfds
    fd = None
    for res in socket.getaddrinfo(None, 50007,
                                  socket.AF_INET,
                                  socket.SOCK_STREAM, 0,
                                  socket.AI_PASSIVE):
        af, socktype, proto, cannonname, sa = res
        try:
            fd = socket.socket(af, socktype, proto)
        except socket.error as msg:
            fd = None
            continue

        try:
            fd.bind(sa)
            fd.listen(1)
        except socket.error as msg:
            fd.close()
            fd = None
            continue

        break

    if fd is None:
        print "Could not open socket"
        return fd

    readfds.append(fd)
    return fd

#global_master = thread_master()
if __name__ == "__main__":
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(metavar='N', default = 0, type = int,
                        help = 'The COM port (N) that connected to NXT',
                        dest = 'com')
    args = parser.parse_args()'''

    serial = init_serial(3)
    server = init_server()

    try:
        while (1):
            if (serial != None):
                serial_read(serial)

            read_ready, write_ready, except_ready = \
                    select.select(readfds, [], [], 1)
            for sock in read_ready:
                if sock == server:
                    server_accept(sock)
                else:
                    client_read(sock)
    except KeyboardInterrupt:
        pass