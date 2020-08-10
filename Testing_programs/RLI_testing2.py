#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port
import time
from sys import stderr 
ev3 = EV3Brick()
colourLeft = ColorSensor(Port.S2)
def RLI_testing2():
    x=0
    start_time = time.time()
    while time.time() < start_time + 1:
        RLI = colourLeft.reflection()
        x = x+1
    print(x, file=stderr)