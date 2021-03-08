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
Testing that the gyro recalibrates correctly when only recalibrated inside a thread 
"""
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from gyroTest_function import idkThread

is_complete = 0
os.environ['IS_COMPLETE'] = str(is_complete)
def main2():
    threadPool = {} 
    stopProcessing = False
    threadKey = 1
    is_complete = os.environ['IS_COMPLETE']

    thread = threading.Thread(target = idkThread, args=(threadKey, gyro)) # gyro entry is a variation
    thread.start()
    threadPool[threadKey] = thread
    threadKey = threadKey+1 

    
    print(threadPool, file=stderr)
    while threadPool:
        is_complete = int(os.environ['IS_COMPLETE'])
        if is_complete != 0: 
            del threadPool[is_complete]
            is_complete = 0
            os.environ['IS_COMPLETE'] = str(is_complete)
            print("deleted thread", file=stderr)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# call function when test starts 
checkGyro = False
sec = 0
while True:
    if Button.CENTER in ev3.buttons.pressed():
        time.sleep(1)
        main2()
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
# test if the gyro only creeps when first being moved 
sec = 0
print("turn the robot")
'''while True:
    if Button.CENTER in ev3.buttons.pressed():
        time.sleep(2)
        break'''
time.sleep(10)
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