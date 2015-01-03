# -*- coding: utf-8 -*-
__author__ = 'sam'

import re

a = "R228G9B1R250G15B0R252G22B0R220G7B1R240G12B0R251G13B0R201G4B0R221G6B0R235G6B0"

class rgb_object:
    def __init__(self):
        self.red = 0
        self.green = 0
        self.blue = 0

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

p = re.compile(r"(?<=R)\d*|(?<=G)\d*|(?<=B)\d*")
p1 = re.compile(r"R\d*|G\d*|B\d*")
red_re = re.compile(r"(?<=R)\d*")
green_re = re.compile(r"(?<=G)\d*")
blue_re = re.compile(r"(?<=B)\d*")
nums = p.findall(a)
num1 = p1.findall(a)

#print nums
print num1

reds = red_re.findall(a)
greens = green_re.findall(a)
blues = blue_re.findall(a)

face_u = []

for red in reds:
    r = int(red)
    rgb = rgb_object()
    rgb.setRed(r)
    face_u.append(rgb)

i = 0
for green in greens:
    g = int(green)
    rgb = face_u[i]
    rgb.setGreen(g)
    i += 1

i = 0
for blue in blues:
    b = int(blue)
    rgb = face_u[i]
    rgb.setBlue(b)
    i += 1

for objects in face_u:
    print "r:%d g:%d b:%d" % (objects.getRed(), objects.getGreen(), objects.getBlue())
'''
for number in nums[::-1]:
    print int(number),
'''

