# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import with_statement

__author__ = 'Gang.Wang'

import socket
import select
import sys

class thread_master:
    readfds = []
    writefds = []

    read_list = []
    write_list = []
    event_list = []
    ready_list = []

    def __init__(self):
        pass

    def add_thread(self, thread, fd):
        self.readfds.append(fd)
        self.read_list.append(thread)

class thread:
    def __init__(self):
        pass

    def add_read(self, tm, fd, func, *args):
        self.func = func
        self.args = args
        self.fd = fd
        self.master = tm

        tm.add_thread(self, fd)

    def run(self):
        self.func(self.args)

def test_read(args):
    print "Hello, I'm the test thread",
    for arg in args:
        print arg

global_master = thread_master()
if __name__ == "__main__":
    test_thread = thread()
    test_thread.add_read(global_master, 1, test_read, "something", "anything")

    for t in global_master.read_list:
        t.run()