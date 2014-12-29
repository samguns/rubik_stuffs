# -*- coding: utf-8 -*-
__author__ = 'sam'
'''
An echo server that uses select to handle multiple clients at a time.
Entering any line of input at the terminal will exit the server.
'''
import select
import socket
import sys

host = None
port = 50007
server = None
size = 1024
for res in socket.getaddrinfo(host, port, socket.AF_INET,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        server = socket.socket(af, socktype, proto)
    except socket.error as msg:
        server = None
        continue
    try:
        server.bind(sa)
        server.listen(1)
    except socket.error as msg:
        server.close()
        server = None
        continue
    break

if server is None:
    print 'could not open socket'
    sys.exit(1)

input = [server]
output = []
error_fd = []
running = 1
while running:
    inputready = []
    try:
        inputready,outputready,exceptready = select.select(input, output, error_fd, 2)
    except KeyboardInterrupt:
        running = 0

    for s in inputready:

        if s == server:
            # handle the server socket
            client, address = server.accept()
            input.append(client)

        else:
            # handle all other sockets
            data = s.recv(size)
            if data:
                print repr(data)
            else:
                s.close()
                input.remove(s)
server.close()