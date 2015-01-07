# -*- coding: utf-8 -*-

__author__ = 'Gang.Wang'

import socket
import select
import sys
import argparse
import re
import urllib2
from ctypes import *
from serial import *
from HTMLParser import HTMLParser

readfds = []
android = None
nxt = None
U = 0
F = 1
D = 2
B = 3
R = 4
L = 5
TURN_180 = 1
COUNTER_CLOCKWISE = 1

face_u = []
face_f = []
face_d = []
face_b = []
face_r = []
face_l = []
color_map = {}
red_re = re.compile(r"(?<=R)\d*")
green_re = re.compile(r"(?<=G)\d*")
blue_re = re.compile(r"(?<=B)\d*")

class rgb_object:
    def __init__(self):
        self.red = 0
        self.green = 0
        self.blue = 0
        self.hue = 0
        self.sat = 0
        self.val = 0
        self.lum = 0

    def setRed(self, r):
        self.red = r

    def getRed(self):
        return self.red

    def setGreen(self, g):
        self.green = g

    def getGreen(self):
        return self.green

    def setBlue(self, b):
        self.blue = b

    def getBlue(self):
        return self.blue

    def getHue(self):
        return self.hue

    def getSat(self):
        return self.sat

    def getVal(self):
        return self.val

    def getLum(self):
        return self.lum

    def rgb_to_hslv(self):
        rgb_min = min(self.red, self.green, self.blue)
        rgb_max = max(self.red, self.green, self.blue)
        c_ubye_max = c_ubyte(rgb_max)
        c_ubye_min = c_ubyte(rgb_min)
        delta = c_ubyte(c_ubye_max.value - c_ubye_min.value)
        g = c_ubyte(self.green)
        r = c_ubyte(self.red)
        b = c_ubyte(self.blue)
        hue = c_ubyte(0)
        self.val = c_ubye_max.value

        if self.val == 0:
            self.hue = self.sat = self.lum = 0
            return

        self.sat = 255 * (long)(delta.value) / self.val
        if (self.sat == 0):
            self.hue = 0
            return

        if (rgb_max == self.red):
            hue.value = 0 + 43 * (g.value - b.value) / delta.value
        elif (rgb_max == self.green):
            hue.value = 85 + 43 * (g.value - r.value) / delta.value
        else:
            hue.value = 171 + 43 * (r.value - g.value) / delta.value

        self.hue = hue.value
        self.lum = (rgb_max + rgb_min) / 2
        return

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

def nxt_write(msg_string):
    msg = str('\x00\x80\x09\x05')
    msg_len = len(msg_string) + 1
    total_msg_len = msg_len + 4
    msg += to_bytes([msg_len])

    for move_byte in msg_string:
        msg += to_bytes([move_byte])

    msg += '\x00'
    nxt_bt_msg = to_bytes([total_msg_len]) + msg
    print repr(nxt_bt_msg)

    try:
        nxt.write(nxt_bt_msg)
    except:
        pass


def get_scaned_colors(face):
    face_list = []
    reds = red_re.findall(face)
    greens = green_re.findall(face)
    blues = blue_re.findall(face)
    for red in reds:
        r = int(red)
        rgb = rgb_object()
        rgb.setRed(r)
        face_list.append(rgb)

    i = 0
    for green in greens:
        g = int(green)
        rgb = face_list[i]
        rgb.setGreen(g)
        i += 1

    i = 0
    for blue in blues:
        b = int(blue)
        rgb = face_list[i]
        rgb.setBlue(b)
        rgb.rgb_to_hslv()
        i += 1

    return face_list

X1 = 0
X2 = 1
X3 = 2
X4 = 3
X5 = 4
X6 = 5
X7 = 6
X8 = 7
X9 = 8
color_U = ""
color_F = ""
color_D = ""
color_B = ""
color_L = ""
color_R = ""

class myparser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = ""

    def handle_data(self, data):
        data = data.strip("\r\n")
        if len(data):
            self.data = data

    def get_data(self):
        return self.data

def generate_facelet_str(facelet):
    str = ""
    for face in facelet:
        if face == color_U:
            str += 'u'
        elif face == color_F:
            str += 'f'
        elif face == color_D:
            str += 'd'
        elif face == color_B:
            str += 'b'
        elif face == color_L:
            str += 'l'
        elif face == color_R:
            str += 'r'

    return str

def generate_nxt_moves(moves):
    moves += 's'
    moves = moves.replace(' ', 's')
    moves = moves.replace('\'', 'n')

    nxt_moves = []
    nxt_byte = 0
    for move in moves:
        print move,
        if move == 'U':
            nxt_byte |= U << 2
        elif move == 'F':
            nxt_byte |= F << 2
        elif move == 'D':
            nxt_byte |= D << 2
        elif move == 'B':
            nxt_byte |= B << 2
        elif move == 'R':
            nxt_byte |= R << 2
        elif move == 'L':
            nxt_byte |= L << 2
        elif move == '2':
            nxt_byte |= TURN_180 << 1
        elif move == 'n':
            nxt_byte |= COUNTER_CLOCKWISE
        elif move == 's':
            nxt_moves.append(nxt_byte)
            nxt_byte = 0

    return nxt_moves

def validate_and_solve(cube):
    global color_U, color_F, color_D, color_B, color_L, color_R

    U_colors = cube[0:9]
    F_colors = cube[9:18]
    D_colors = cube[18:27]
    B_colors = cube[27:36]
    L_colors = cube[36:45]
    R_colors = cube[45:54]
    color_U = U_colors[X5]
    color_F = F_colors[X5]
    color_D = D_colors[X5]
    color_B = B_colors[X5]
    color_L = L_colors[X5]
    color_R = R_colors[X5]

    url_str = "http://127.0.0.1:8081/?"
    url_str += generate_facelet_str(U_colors)
    url_str += generate_facelet_str(R_colors)
    url_str += generate_facelet_str(F_colors)
    url_str += generate_facelet_str(D_colors)
    url_str += generate_facelet_str(L_colors)
    url_str += generate_facelet_str(B_colors)
    print url_str

    cube = urllib2.urlopen(url_str)
    cube_string = cube.read()
    parser = myparser()
    parser.feed(cube_string)
    print repr(parser.get_data())
    parser.close()

    generate_nxt_moves(parser.get_data())

def sample_color(android_bmp_data):
    global face_u, face_f, face_d, face_b, face_r, face_l
    global current_face

    if (current_face == U):
        face_u = get_scaned_colors(android_bmp_data)
    elif (current_face == F):
        face_f = get_scaned_colors(android_bmp_data)
    elif (current_face == D):
        face_d = get_scaned_colors(android_bmp_data)
    elif (current_face == B):
        face_b = get_scaned_colors(android_bmp_data)
    elif (current_face == L):
        face_l = get_scaned_colors(android_bmp_data)
    elif (current_face == R):
        face_r = get_scaned_colors(android_bmp_data)

def sort_cube_colors():
    all_faces = []
    for items in face_u:
        all_faces.append(items)

    for items in face_f:
        all_faces.append(items)

    for items in face_d:
        all_faces.append(items)

    for items in face_b[::-1]:
        all_faces.append(items)

    for items in face_l:
        all_faces.append(items)

    for items in face_r[::-1]:
        all_faces.append(items)

    all_faces_hue_map = {}
    i = 0
    for items in all_faces:
        all_faces_hue_map.setdefault(items.getHue(), []).append(i)
        print i, "r:", items.getRed(), "g:", items.getGreen(), "b:", items.getBlue(), \
                "hue:", items.getHue(), "sat:", items.getSat(), "val:", items.getVal(), "lum:", items.getLum()
        i += 1

    color_table = []
    sorted_hue_keys = sorted(all_faces_hue_map.keys(), reverse=True)
    for hue_key in sorted_hue_keys:
        print hue_key,
        for items in all_faces_hue_map[hue_key]:
            color_table.append(items)
            print items,
        print " "

    red_faces = color_table[0:9]
    blue_faces = color_table[9:18]
    green_faces = color_table[18:27]
    white_faces = color_table[27:36]
    yellow_faces = color_table[36:45]
    orange_faces = color_table[45:54]

    print "red", sorted(red_faces)
    print "orange", sorted(orange_faces)
    print "yellow", sorted(yellow_faces)
    print "green", sorted(green_faces)
    print "blue", sorted(blue_faces)
    print "white", sorted(white_faces)
    print "########"

    red_faces_final = []
    blue_faces_final = []
    green_faces_final = []
    white_faces_final = []
    yellow_faces_final = []
    orange_faces_final = []
    global color_map
    for red in red_faces:
        if all_faces[red].getGreen() >= all_faces[red].getBlue():
            orange_faces_final.append(red)
            color_map[red] = "O"
        else:
            red_faces_final.append(red)
            color_map[red] = "R"

    for orange in orange_faces:
        if all_faces[orange].getBlue() >= all_faces[orange].getGreen():
            red_faces_final.append(orange)
            color_map[orange] = "R"
        else:
            orange_faces_final.append(orange)
            color_map[orange] = "O"

    for blue in blue_faces:
        red_t = all_faces[blue].getRed()
        green_t = all_faces[blue].getGreen()
        blue_t = all_faces[blue].getBlue()
        rgb_max = max(red_t, green_t, blue_t)
        if (rgb_max == blue_t) and (red_t + green_t < blue_t):
            blue_faces_final.append(blue)
            color_map[blue] = "B"
        elif (rgb_max == green_t) and (red_t + blue_t < green_t):
            green_faces_final.append(blue)
            color_map[blue] = "G"
        else:
            white_faces_final.append(blue)
            color_map[blue] = "W"

    for green in green_faces:
        red_t = all_faces[green].getRed()
        green_t = all_faces[green].getGreen()
        blue_t = all_faces[green].getBlue()
        rgb_max = max(red_t, green_t, blue_t)
        if (rgb_max == green_t) and (red_t + blue_t < green_t):
            green_faces_final.append(green)
            color_map[green] = "G"
        elif (rgb_max == blue_t) and (red_t + green_t < blue_t):
            blue_faces_final.append(green)
            color_map[green] = "B"
        else:
            white_faces_final.append(green)
            color_map[green] = "W"

    for yellow in yellow_faces:
        if all_faces[yellow].getSat() < 50:
            white_faces_final.append(yellow)
            color_map[yellow] = "W"
        else:
            yellow_faces_final.append(yellow)
            color_map[yellow] = "Y"

    for white in white_faces:
        red_t = all_faces[white].getRed()
        green_t = all_faces[white].getGreen()
        blue_t = all_faces[white].getBlue()
        rgb_max = max(red_t, green_t, blue_t)
        if (red_t + green_t > blue_t) and \
                (red_t + blue_t > green_t) and \
                (green_t + blue_t > red_t):
            white_faces_final.append(white)
            color_map[white] = "W"
        elif (rgb_max == green_t) and \
                (red_t + blue_t < green_t) and \
                (2 * (blue_t + red_t) < green_t):
            green_faces_final.append(white)
            color_map[white] = "G"
        else:
            yellow_faces_final.append(white)
            color_map[white] = "Y"

    print "red", sorted(red_faces_final)
    print "orange", sorted(orange_faces_final)
    print "yellow", sorted(yellow_faces_final)
    print "green", sorted(green_faces_final)
    print "blue", sorted(blue_faces_final)
    print "white", sorted(white_faces_final)

    cube = []
    sorted_color_map_keys = sorted(color_map.keys())
    for index in sorted_color_map_keys:
        print "face:", index, "color:", color_map[index]
        cube.append(color_map[index])

    validate_and_solve(cube)

def process_data(fd, data):
    global android
    global temp
    global face_u, face_f, face_d, face_b, face_r, face_l
    global current_face

    if (fd != android):
        if (data == "U"):
            current_face = U
            android.sendall("scan U\n")
        elif (data == "F"):
            current_face = F
            android.sendall("scan F\n")
        elif (data == "D"):
            current_face = D
            android.sendall("scan D\n")
        elif (data == "B"):
            current_face = B
            android.sendall("scan B\n")
        elif (data == "R"):
            current_face = R
            android.sendall("scan R\n")
        elif (data == "L"):
            current_face = L
            android.sendall("scan L\n")
        elif (data == "end"):
            sort_cube_colors()
            #solve_cube()
            face_u = face_f = face_d = face_b = face_r = face_l = ""
            current_face = 255
            fd.sendall("Acknowledge!")
    else:
        sample_color(data)
        temp.sendall("Roger that!")

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
    client, address = server.accept()
    print "Connected by", address, client
    readfds.append(client)

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

    global nxt
    nxt = init_serial(3)
    server = init_server()

    try:
        while True:
            if nxt != None:
                serial_read(nxt)

            read_ready, write_ready, except_ready = \
                                select.select(readfds, [], [], 1)
            for sock in read_ready:
                if sock == server:
                    server_accept(sock)
                else:
                    client_read(sock)
    except KeyboardInterrupt:
        pass