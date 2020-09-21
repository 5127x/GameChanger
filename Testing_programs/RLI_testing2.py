#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port
import time
import threading
from sys import stderr 
import os

ev3 = EV3Brick()
colourRight = ColorSensor(Port.S2)



def RLI_testing2(threadKey):
    print('sdfg', file=stderr)

    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    x=0
    start_time = time.time()
    while time.time() < start_time + 1:
        RLI = colourRight.reflection()
        x = x+1
    print(x, file=stderr)
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
    print(is_complete, file=stderr)