#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import GyroSensor
from pybricks.parameters import Port, Button
import time
import threading
from sys import stderr 
import os

ev3 = EV3Brick()
gyro = GyroSensor(Port.S4)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""
test if resetting the gyro actually works 
"""

# FINISHED 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

while True:
    if Button.CENTER in ev3.buttons.pressed():
        break

g = gyro.angle()
print("initial gyro reading {}".format(g))
time.sleep(5)

gyro.reset_angle(0)
g = gyro.angle() 
print("reset attempt #1.1 {}".format(g))
time.sleep(5)
g = gyro.angle()
print("reset attempt #1.2 {}".format(g))

gyro.reset_angle(180)
g = gyro.angle()
print("reset attempt random number #1.1 {}".format(g))
time.sleep(5)
g = gyro.angle()
print("reset attempt random number #1.2 {}".format(g))

gyro.reset_angle(0)
g = gyro.angle()
print("reset attempt #2.1 {}".format(g))
time.sleep(5)
g = gyro.angle()
print("reset attempt #2.2 {}".format(g))
time.sleep(5)