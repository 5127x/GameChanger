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
Testing that the gyro recalibrates correctly within one file  
"""

# FINISHED, VARIATIONS CONTINUEING 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# call function when test starts 
checkGyro = False
beforeGyro = []
afterGyro = []
otherGyro = []
rep = 0
while True:
    if rep != 20:
        time.sleep(1)
        
        x = gyro.angle()
        beforeGyro.append(x)
        gyro.speed()
        gyro.angle()
        gyro.reset_angle(0) # variation line
        y = gyro.angle()
        afterGyro.append(y)

        time.sleep(5)
        z = gyro.angle()
        otherGyro.append(z)
        rep = rep +1
        print(rep)
    else:
        break

print(beforeGyro)
print(afterGyro)
print(otherGyro)
print(" ")
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""
result 1:
[-32, 2110, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # wtf happened here??? confusion
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[2142, 31, 31, 32, 32, 31, 32, 31, 32, 32, 31, 32, 32, 32, 32, 32, 32, 32, 31, 32]
"""