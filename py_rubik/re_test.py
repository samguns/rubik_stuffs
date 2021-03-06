# -*- coding: utf-8 -*-
__author__ = 'sam'

import re
import urllib2
from ctypes import *
from HTMLParser import HTMLParser

#Orange
#B = "R227G41B0R210G28B0R203G25B0R225G37B0R201G33B2R201G31B1R224G30B0R202G25B1R189G23B5"
B = "R189G209B0R234G3B94R6G61B129R180G199B1R240G10B0R251G7B3R140G144B147R0G40B120R231G0B91"
#White
#D = "R191G187B178R171G168B159R164G161B152R186G187B179R161G162B154R160G161B153R189G190B182R162G167B161R145G148B141"
D = "R230G0B88R253G14B0R250G16B1R0G41B127R174G189B189R0G72B159R0G143B0R163G173B174R182G190B192"
#Red
F = "R222G0B75R243G0B96R0G187B2R0G138B0R229G0B80R243G1B101R137G142B148R0G144B0R197G210B0"
#F = "R227G27B84R212G18B68R208G17B69R229G18B80R207G21B66R206G20B68R220G17B81R203G16B65R189G17B59"
#Yellow
U = "R1G36B104R176G197B0R164G181B14R149G161B0R161G182B0R150G169B175R0G97B0R157G169B0R217G5B0"
#U = "R178G179B0R154G159B0R146G153B0R177G181B0R143G149B2R142G152B0R177G185B0R150G158B0R136G141B0"
#Green
R = "R250G6B0R254G0B125R2G93B186R171G179B181R0G186B4R1G205B4R0G41B124R0G52B140R194G199B202"
#R = "R0G170B23R0G150B10R0G142B11R0G168B11R2G137B12R0G142B14R0G172B16R1G151B21R3G134B22"
#Blue
L = "R227G1B84R252G12B4R228G243B0R0G143B1R0G51B143R184G195B204R215G1B0R231G5B0R3G164B4"
#L = "R0G120B193R0G97B175R0G90B167R0G115B191R0G95B168R0G98B166R0G119B197R0G97B174R0G91B161"

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

p = re.compile(r"(?<=R)\d*|(?<=G)\d*|(?<=B)\d*")
p1 = re.compile(r"R\d*|G\d*|B\d*")
red_re = re.compile(r"(?<=R)\d*")
green_re = re.compile(r"(?<=G)\d*")
blue_re = re.compile(r"(?<=B)\d*")
nums = p.findall(U)
num1 = p1.findall(U)


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
U_colors = []
F_colors = []
D_colors = []
B_colors = []
L_colors = []
R_colors = []
color_U = ""
color_F = ""
color_D = ""
color_B = ""
color_L = ""
color_R = ""

def check_edge(face_1, face_2, pos1, pos2, color_1, color_2):
    if color_1 == face_1[pos1]:
        if color_2 == face_2[pos2]:
            return 1
    elif color_2 == face_2[pos1]:
        if color_1 == face_1[pos2]:
            return 1
    else:
        return -1

def find_edge(color_1, color_2):
    if check_edge(U_colors, F_colors, X8, X2, color_1, color_2) > 0 or \
            check_edge(U_colors, R_colors, X6, X2, color_1, color_2) > 0 or \
            check_edge(U_colors, B_colors, X2, X2, color_1, color_2) > 0 or \
            check_edge(U_colors, L_colors, X4, X2, color_1, color_2) > 0 or \
            check_edge(D_colors, F_colors, X2, X8, color_1, color_2) > 0 or \
            check_edge(D_colors, R_colors, X6, X8, color_1, color_2) > 0 or \
            check_edge(D_colors, B_colors, X8, X8, color_1, color_2) > 0 or \
            check_edge(D_colors, L_colors, X4, X8, color_1, color_2) > 0 or \
            check_edge(F_colors, R_colors, X6, X4, color_1, color_2) > 0 or \
            check_edge(F_colors, L_colors, X4, X6, color_1, color_2) > 0 or \
            check_edge(B_colors, R_colors, X4, X6, color_1, color_2) > 0 or \
            check_edge(B_colors, L_colors, X6, X4, color_1, color_2) > 0:
        return 1

    return -1

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

def validate_cube():
    if find_edge(color_U, color_F) < 0:
        print "Invalid scanned cube"

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

if __name__ == "__main__":
    face_u = get_scaned_colors(U)
    face_f = get_scaned_colors(F)
    face_d = get_scaned_colors(D)
    face_b = get_scaned_colors(B)
    face_l = get_scaned_colors(L)
    face_r = get_scaned_colors(R)

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

    i = 0
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

    print "red", red_faces
    print "orange", orange_faces
    print "yellow", yellow_faces
    print "green", green_faces
    print "blue", blue_faces
    print "white", white_faces
    print "########"

    red_faces_final = []
    blue_faces_final = []
    green_faces_final = []
    white_faces_final = []
    yellow_faces_final = []
    orange_faces_final = []
    color_map = {}
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

    sorted_color_map_keys = sorted(color_map.keys())
    color_list = []
    for index in sorted_color_map_keys:
        print "face:", index, "color:", color_map[index]
        color_list.append(color_map[index])

    global U_colors, F_colors, D_colors, B_colors, L_colors, R_colors
    global color_U, color_F, color_D, color_B, color_L, color_R
    U_colors = color_list[0:9]
    F_colors = color_list[9:18]
    D_colors = color_list[18:27]
    B_colors = color_list[27:36]
    L_colors = color_list[36:45]
    R_colors = color_list[45:54]
    color_U = U_colors[X5]
    color_F = F_colors[X5]
    color_D = D_colors[X5]
    color_B = B_colors[X5]
    color_L = L_colors[X5]
    color_R = R_colors[X5]
    print "u", "[", color_U, "]", U_colors
    print "f", "[", color_F, "]", F_colors
    print "d", "[", color_D, "]", D_colors
    print "b", "[", color_B, "]", B_colors
    print "l", "[", color_L, "]", L_colors
    print "r", "[", color_R, "]", R_colors

    validate_cube()

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