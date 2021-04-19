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

# SMTH IS WRONG WITH THE CODE, FIND AND FIX LATER 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def calibrateTest(threadKey):
    print("calTest1", file=stderr)
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    gyro.speed()
    gyro.angle()

    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
is_complete = 0
os.environ['IS_COMPLETE'] = str(is_complete)
def main():
    threadPool = {} 
    stopProcessing = False
    threadKey = 1
    is_complete = os.environ['IS_COMPLETE']

    x = gyro.angle()

    thread = threading.Thread(target = calibrateTest, args=(threadKey, ))
    thread.start()
    threadPool[threadKey] = thread
    threadKey = threadKey+1 
    
    print(threadPool, file=stderr)
    s_time = time.time()
    x_time = s_time+3
    sec = 0
    while threadPool:
        is_complete = int(os.environ['IS_COMPLETE'])
        if is_complete != 0: 
            del threadPool[is_complete]
            is_complete = 0
            os.environ['IS_COMPLETE'] = str(is_complete)
            print("deleted thread", file=stderr)
    
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
while True:
    if Button.CENTER in ev3.buttons.pressed():
        break
a = gyro.angle()
time.sleep(5)
b = gyro.angle()
print("5 sec apart readings: {} and {}".format(a,b))
main()

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