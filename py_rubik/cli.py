# -*- coding: utf-8 -*-
__author__ = 'sam'

import socket

host = raw_input("Connect to --> ")
port = 50007
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
s.send('Hello, world')
s.close()