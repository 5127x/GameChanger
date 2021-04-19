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

# cant calibrate n4 sensors in python as far as we are aware 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# call function when test starts 
checkGyro = False
sec = 0
while True:
    if Button.CENTER in ev3.buttons.pressed():
        print(gyro.angle())
        time.sleep(1)
        x = gyro.angle()

        """
        try:
            gyro.distance()
            gyro.keypad()
        except:
            print("nup")

        try: 
            InfraredSensor(Port.S4)
        except:
            print("nup")"""
         

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