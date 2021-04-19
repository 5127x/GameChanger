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
Testing how long it takes for the gyro to stabalise and read as 0 instead of a random number 
"""

# F 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# basic function to recalibrate the gyro 
def idk():
    x = gyro.angle()
    gyro.speed()
    gyro.angle()
    y = gyro.angle()
    
    start = time.time()
    end = start + 3
    array = []
    while time.time() < end:
        g = gyro.angle()
        array.append(g)

    print(array)
    print("gyro readings immediately before and after recalibration: {}, {}".format(x,y))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# call function when test starts 

while True:
    if Button.CENTER in ev3.buttons.pressed():
        time.sleep(1)
        idk()
        time.sleep(0.5)
        break
