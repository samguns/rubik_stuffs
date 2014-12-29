# -*- coding: utf-8 -*-
__author__ = 'sam'
'''
An echo server that uses select to handle multiple clients at a time.
Entering any line of input at the terminal will exit the server.
'''
import select
import socket


host = '127.0.0.1'
port = 50007

size = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen(5)
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