# -*- coding: utf-8 -*-
__author__ = 'sam'

import socket

host = '127.0.0.1'
port = 50007
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
s.send('Hello, world')
s.close()