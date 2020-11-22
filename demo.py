#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import ColorSensor, GyroSensor, Motor
from pybricks.parameters import Port
from pybricks.media.ev3dev import SoundFile
from Functions_Completed.waiting import waiting
import os
from sys import stderr
import time 
largeMotor_Right = Motor(Port.B)
largeMotor_Left = Motor(Port.C)
panel = Motor(Port.D)
print("Motors Connected", file = stderr)

gyro = GyroSensor(Port.S1)
colourRight = ColorSensor(Port.S2)
colourLeft = ColorSensor(Port.S3)
colourkey = ColorSensor(Port.S4)
print("Sensors Connected", file = stderr)


ev3 = EV3Brick()
'''
#test for gyro creep
while True:
    time.sleep(0.5)
    rli = colourRight.reflection()
    print(rli, file=stderr)

time.sleep(5)
'''

x=False 
'''
while True: 
    print(gyro.angle())
    waiting(lambda:x, 0, 0.5)
'''

rgbRed = colourkey.rgb()
print("red", file=stderr)
time.sleep(3)
rgbEmpty = colourkey.rgb()
print("done")

print(rgbRed, file=stderr)
print(rgbEmpty, file=stderr)

'''
rgbWhite = colourkey.rgb()
print("NEXT", file=stderr)
waiting(lambda:x, 0, 4)
rgbYellow = colourkey.rgb()
print("NEXT", file=stderr)
waiting(lambda:x, 0, 4)
rgbRed = colourkey.rgb()
print("NEXT", file=stderr)
waiting(lambda:x, 0, 4)
rgbBlue = colourkey.rgb()
print("NEXT", file=stderr)
waiting(lambda:x, 0, 4)
rgbEmpty = colourkey.rgb()
print("NEXT", file=stderr)
waiting(lambda:x, 0, 4)
rgbGreen = colourkey.rgb()
print("DONE", file=stderr)

print(rgbWhite, file=stderr)
print(rgbYellow, file=stderr)
print(rgbRed, file=stderr)
print(rgbBlue, file=stderr)
print(rgbEmpty, file=stderr)
print(rgbGreen, file=stderr)
# 1. white
# 2. yellow
# 3. red 
# 4. blue
'''

'''
(69, 99, 100) white 
(61, 56, 16) yellow
(44, 13, 9) red
(6, 24, 63) blue
(12, 19, 27) empty
(6, 33, 14) green
'''