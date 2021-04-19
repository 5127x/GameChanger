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

# NEED TO TEST

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# basic function to recalibrate the gyro 
'''
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
        break'''
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def calibrateTest(threadKey):
    print("calTest1", file=stderr)
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    print(gyro.angle())
    gyro.speed()
    gyro.angle()

    print("calTest2", file=stderr)
    start1 = time.time()
    end1 = start1 + 3
    array1 = []
    while time.time() < end1:
        if time.time() > start1 + 0.01:
            #print(".")
            g1 = gyro.angle()
            array1.append(g1)
            start1 = time.time()
    print("f1: {}".format(array1))

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

    thread = threading.Thread(target = calibrateTest, args=(threadKey, ))
    thread.start()
    threadPool[threadKey] = thread
    threadKey = threadKey+1 
    
    print(threadPool, file=stderr)
    start2 = time.time()
    end2 = start2 + 3
    array2 = []
    while threadPool:
        is_complete = int(os.environ['IS_COMPLETE'])
        if is_complete != 0: 
            del threadPool[is_complete]
            is_complete = 0
            os.environ['IS_COMPLETE'] = str(is_complete)
            print("deleted thread", file=stderr)
        
        if time.time() < end2:
            if time.time() > start2 + 0.01:
                g2 = gyro.angle()
                array2.append(g2)
                start2 = time.time() 
    print("f2: {}".format(array2))


time.sleep(4)
a = gyro.angle()
time.sleep(5)
b = gyro.angle()
print("5 sec apart readings: {} and {}".format(a,b))
main()
print(gyro.angle())