# -*- coding: utf-8 -*-
__author__ = 'sam'

import re

#Orange
U = "R227G41B0R210G28B0R203G25B0R225G37B0R201G33B2R201G31B1R224G30B0R202G25B1R189G23B5"
#White
F = "R191G187B178R171G168B159R164G161B152R186G187B179R161G162B154R160G161B153R189G190B182R162G167B161R145G148B141"
#Red
D = "R227G27B84R212G18B68R208G17B69R229G18B80R207G21B66R206G20B68R220G17B81R203G16B65R189G17B59"
#Yellow
B = "R178G179B0R154G159B0R146G153B0R177G181B0R143G149B2R142G152B0R177G185B0R150G158B0R136G141B0"
#Green
L = "R0G170B23R0G150B10R0G142B11R0G168B11R2G137B12R0G142B14R0G172B16R1G151B21R3G134B22"
#Blue
R = "R0G120B193R0G97B175R0G90B167R0G115B191R0G95B168R0G98B166R0G119B197R0G97B174R0G91B161"

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

    def setHue(self, hue):
        self.hue = hue

    def getHue(self):
        return self.hue

    def setSat(self, sat):
        self.sat = sat

    def getSat(self):
        return self.sat

    def setVal(self, val):
        self.val = val

    def getVal(self):
        return self.val

    def setLum(self, lum):
        self.lum = lum

    def getLum(self):
        return self.lum

    def rgb_to_hslv(self):
        rgb_min = min(self.red, self.green, self.blue)
        rgb_max = max(self.red, self.green, self.blue)
        delta = rgb_max - rgb_min
        self.val = rgb_max

        if self.val == 0:
            self.hue = self.sat = self.lum = 0
            return

        self.sat = 255 * (long)(delta) / self.val
        if (self.sat == 0):
            self.hue = 0
            return

        if (rgb_max == self.red):
            self.hue = 43 * ((self.green - self.blue) % 256) / delta
        elif (rgb_max == self.green):
            self.hue = 85 + 43 * ((self.green - self.red) % 256) / delta
        else:
            self.hue = 171 + 43 * ((self.red - self.green) % 256) / delta

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

    i = 0
    for all in all_faces:
        print i, "r:", all.getRed(), "g:", all.getGreen(), "b:", all.getBlue(), \
                "hue:", all.getHue(), "sat:", all.getSat(), "val:", all.getVal(), "lum:", all.getLum()
        i += 1

'''
face_u_red_map = {}
face_u_green_map = {}
face_u_blue_map = {}


i = 0
for objects in face_u:
    face_u_red_map[objects.getRed()] = i
    face_u_green_map[objects.getGreen()] = i
    face_u_blue_map[objects.getBlue()] = i
    print "r:%d g:%d b:%d" % (objects.getRed(), objects.getGreen(), objects.getBlue())
    i += 1

sorted_red_keys = sorted(face_u_red_map.keys(), reverse=True)
print sorted_red_keys
for red_key in sorted_red_keys:
    print face_u_red_map[red_key]

sorted_green_keys = sorted(face_u_green_map.keys(), reverse=True)
print sorted_green_keys
'''
'''
for number in nums[::-1]:
    print int(number),
'''

