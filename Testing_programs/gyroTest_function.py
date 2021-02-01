#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import GyroSensor
from pybricks.parameters import Port, Button
import time
import threading
from sys import stderr 
import os

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""
Functions used in testing:
- calibrate function w/ before and after
- threading calibrate function w/ before and after
"""
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def idk():
    x = gyro.angle()
    gyro.speed()
    gyro.angle()
    gyro.reset_angle(0)
    y = gyro.angle()
    print("idk before and after: {}, {}".format(x,y))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def idkThread(threadKey):
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    x = gyro.angle()
    gyro.speed()
    gyro.angle()
    gyro.reset_angle(0)
    y = gyro.angle()
    print("idk before and after: {}, {}".format(x,y))

    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -