# -*- coding: utf-8 -*-

from __future__ import with_statement

__author__ = 'Gang.Wang'

import socket
import sys

if __name__ == "__main__":
    s = None

    for res in socket.getaddrinfo("localhost", 50007, socket.AF_INET,
                                  socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue

        try:
            s.connect(sa)
        except socket.error as msg:
            s.close()
            s = None
            continue

        break

    if s is None:
        print "Could not open socket"
        sys.exit(1)

    s.sendall("\x41\x42")
    s.close()