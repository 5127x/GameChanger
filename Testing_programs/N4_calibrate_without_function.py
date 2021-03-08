#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import GyroSensor, InfraredSensor
from pybricks.parameters import Port, Button
import time
import threading
from sys import stderr 
import os

ev3 = EV3Brick()
gyro = GyroSensor(Port.S4)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""
Testing that the gyro recalibrates correctly within one file and outside of a function 
"""

# 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# call function when test starts 
checkGyro = False
sec = 0
while True:
    if Button.CENTER in ev3.buttons.pressed():
        time.sleep(1)
        x = gyro.angle()

        """try to read gyro def as gyro with infrared commands? maybe?"""

        #gyro.reset_angle(180) # CHANGE BACK TO 0
        y = gyro.angle()
        print("gyro readings immediately before and after recalibration: {}, {}".format(x,y))

        checkGyro = True
        time.sleep(2)
        break

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# test if the gyro creeps when not reset 
time.sleep(3)

cur = gyro.angle()
print("Gyro angle starting to check values {}".format(cur))
while checkGyro:
    time.sleep(1)
    g = gyro.angle()
    if cur == g:
        sec = sec + 1
        cur = g
    else:
        break
    if sec == 20:
        print("reached max secs")
        break
print("remained at {} for {} secs after reset".format(g, sec))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# wait for confirmation
sec = 0
print("turn the robot")
time.sleep(10)
'''
while checkGyro:
    if Button.CENTER in ev3.buttons.pressed():
        time.sleep(2)
        break'''

# test if the gyro only creeps when first being moved 
time.sleep(3)

cur = gyro.angle()
print("Gyro angle starting to check values {}".format(cur))
while checkGyro:
    time.sleep(1)
    g = gyro.angle()
    if cur == g:
        sec = sec + 1
        cur = g
    else:
        break
    if sec == 20:
        print("reached max secs")
        break
print("remained at {} for {} secs after being turned".format(g, sec))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -