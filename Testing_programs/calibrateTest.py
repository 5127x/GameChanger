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
Testing if the gyro reads differently in a thread compared to the main file 
Testing/comparing if the gyro reads differently in two threads/functions 
"""
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

is_complete = 0
os.environ['IS_COMPLETE'] = str(is_complete)
def main():
    threadPool = {} 
    stopProcessing = False
    threadKey = 1
    is_complete = os.environ['IS_COMPLETE']

    thread = threading.Thread(target = EVENTUALFUNCTION, args=(threadKey, ))
    thread.start()
    threadPool[threadKey] = thread
    threadKey = threadKey+1 
    
    print(threadPool, file=stderr)
    s_time = time.time()
    sec = 0
    while threadPool:
        is_complete = int(os.environ['IS_COMPLETE'])
        if is_complete != 0: 
            del threadPool[is_complete]
            is_complete = 0
            os.environ['IS_COMPLETE'] = str(is_complete)
            print("deleted thread", file=stderr)
        
        cur_time = time.time()
        if cur_time == s_time + 1:
            sec = sec + 1
            s_time = cur_time 
            x = gyro.angle()
            print("main program file: gyro reads {}, {} seconds in".format(x, sec))
            

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
while True:
    if Button.CENTER in ev3.buttons.pressed():
        break
main()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def calibrateTest():
    gyro.speed()
    gyro.angle()

    s_time = time.time()
    sec = 0
    cur_time = time.time()
    if cur_time == s_time + 1:
        sec = sec + 1
        s_time = cur_time 
        x = gyro.angle()
        print("calibrateTest function: gyro reads {}, {} seconds in".format(x, sec))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def resetTest():
    gyro.reset_angle(0)

    s_time = time.time()
    sec = 0
    cur_time = time.time()
    if cur_time == s_time + 1:
        sec = sec + 1
        s_time = cur_time 
        x = gyro.angle()
        print("resetTest function: gyro reads {}, {} seconds in".format(x, sec))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -