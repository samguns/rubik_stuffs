# -*- coding: utf-8 -*-
__author__ = 'sam'

import re
from ctypes import *

#Orange
#B = "R227G41B0R210G28B0R203G25B0R225G37B0R201G33B2R201G31B1R224G30B0R202G25B1R189G23B5"
B = "R177G7B77R182G6B78R146G182B202R100G140B162R186G9B85R0G143B31R231G24B1R189G211B5R219G14B135"
#White
D = "R191G187B178R171G168B159R164G161B152R186G187B179R161G162B154R160G161B153R189G190B182R162G167B161R145G148B141"
#Red
F = "R227G27B84R212G18B68R208G17B69R229G18B80R207G21B66R206G20B68R220G17B81R203G16B65R189G17B59"
#Yellow
U = "R178G179B0R154G159B0R146G153B0R177G181B0R143G149B2R142G152B0R177G185B0R150G158B0R136G141B0"
#Green
R = "R0G170B23R0G150B10R0G142B11R0G168B11R2G137B12R0G142B14R0G172B16R1G151B21R3G134B22"
#Blue
L = "R0G120B193R0G97B175R0G90B167R0G115B191R0G95B168R0G98B166R0G119B197R0G97B174R0G91B161"

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

    for items in face_b:
        all_faces.append(items)

    for items in face_l:
        all_faces.append(items)

    for items in face_r:
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
        if all_faces[blue].getGreen() >= all_faces[blue].getBlue():
            green_faces_final.append(blue)
            color_map[blue] = "G"
        else:
            blue_faces_final.append(blue)
            color_map[blue] = "B"

    for green in green_faces:
        if all_faces[green].getBlue() >= all_faces[green].getGreen():
            blue_faces.append(green)
            color_map[green] = "B"
        else:
            green_faces_final.append(green)
            color_map[green] = "G"

    for yellow in yellow_faces:
        if all_faces[yellow].getSat() < 50:
            white_faces_final.append(yellow)
            color_map[yellow] = "W"
        else:
            yellow_faces_final.append(yellow)
            color_map[yellow] = "Y"

    for white in white_faces:
        if all_faces[white].getSat() > 50:
            yellow_faces_final.append(white)
            color_map[white] = "Y"
        else:
            white_faces_final.append(white)
            color_map[white] = "W"

    print "red", red_faces_final
    print "orange", orange_faces_final
    print "yellow", yellow_faces_final
    print "green", green_faces_final
    print "blue", blue_faces_final
    print "white", white_faces_final

    sorted_color_map_keys = sorted(color_map.keys())
    for index in sorted_color_map_keys:
        print "face:", index, "color:", color_map[index]
