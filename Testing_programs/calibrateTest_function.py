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
Functions used in testing:
- 
- 
- 
"""
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def calibrateTest(threadKey):
    print("calTest1", file=stderr)
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    print(gyro.angle())
    gyro.speed()
    gyro.angle()
    gyro.reset_angle(0) # variation line 
    print("calTest2", file=stderr)
    time.sleep(3)
    sec = 0
    print("calTest3", file=stderr)
    while True:
        time.sleep(1)
        sec = sec + 1
        x = gyro.angle()
        print("calibrateTest function: gyro reads {}, {} seconds in".format(x, sec), file=stderr)
        if sec ==40:
            print('40 sec')
            break

    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -