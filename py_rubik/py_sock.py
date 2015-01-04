# -*- coding: utf-8 -*-

from __future__ import with_statement

__author__ = 'Gang.Wang'

import socket
import select
import sys

if __name__ == "__main__":
    s = None
    i = 0
    running = 1
    input = []

    for res in socket.getaddrinfo(None, 50007, socket.AF_INET,
                                  socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, cannonname, sa = res
        print "af %d, socktype %d proto %d" % (af, socktype, proto)
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue

        try:
            s.bind(sa)
            s.listen(1)
        except socket.error as msg:
            s.close()
            s = None
            continue

        input.append(s)

        break

    if s is None:
        print "Could not open socket"
        sys.exit(1)

    while running:
        read_ready = []
        try:
            read_ready, write_ready, except_ready = select.select(input, [], [], 2)
        except KeyboardInterrupt:
            running = 0

        for in_sock in read_ready:
            if in_sock == s:
                client, address = s.accept()
                print 'Connected by', address, client
                input.append(client)

            else:
                data = in_sock.recv(1024)
                if not data:
                    in_sock.close()
                    input.remove(in_sock)
                    print "Closing ", in_sock
                else:
                    hello_str = "Hello" + str(i) + "\n"
                    in_sock.sendall(hello_str)
                    print repr(data)
                    i += 1

    s.close()
