# -*- coding: utf-8 -*-
__author__ = 'sam'

import pygame
import math
from serial import *

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

nxt_data_prefix = '\x0a\x00\x80\x09\x00\x06'

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputing the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def printf(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

# Connect to NXT via Bluetooth serial COM port

pygame.init()
ser = Serial()
ser.port = 3
ser.timeout = 300
if False == ser.isOpen():
    ser.open()

# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("NXT Bluetooth Remote Control")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Get ready to print
textPrint = TextPrint()

# Main loop
while done == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(WHITE)
    textPrint.reset()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    name = joystick.get_name()
    textPrint.printf(screen, "Joystick: {}".format(name))

    forward_raw = joystick.get_axis(3)
    if 0 != forward_raw:
        fb = '\x00'
        power_level = int(forward_raw * 100)
        if (power_level < 0):
            sign = '\x01'
            power_level = abs(power_level)
        else:
            sign = '\x00'

        nxt_motor_data = nxt_data_prefix + fb + '\x00' + \
                         sign + '\x00' + \
                         to_bytes([power_level]) + '\x00'
        ser.write(nxt_motor_data)

    steering_raw = joystick.get_axis(0)
    if 0 != steering_raw:
        lr = '\x01'
        steering = int(steering_raw * 100)
        if (steering < 0):
            sign = '\x01'
            steering = abs(steering)
        else:
            sign = '\x00'

        nxt_motor_data = nxt_data_prefix + lr + '\x00' + \
                         sign + '\x00' + \
                         to_bytes([steering]) + '\x00'
        ser.write(nxt_motor_data)

    axes = joystick.get_numaxes()
    for i in range(axes):
        axis = joystick.get_axis(i)
        textPrint.printf(screen, "Axis {} value: {:>d}".format(i, int(axis * 100)))
    textPrint.unindent()

    pygame.display.flip()
    clock.tick(20)

pygame.quit()
ser.close()