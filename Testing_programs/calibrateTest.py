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
def calibrateTest(threadKey):
    print("calTest1", file=stderr)
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    print(gyro.angle())
    gyro.speed()
    gyro.angle()
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
def resetTest(threadKey):
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])
    
    print("start reset")
    gyro.reset_angle(0)
    print("reset done")
    print(time.time())

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
        
        cur_time = time.time()
        if cur_time >= s_time + 1 and cur_time >= x_time:
            sec = sec + 1
            s_time = s_time +1 
            x = gyro.angle()
            print("main program file: gyro reads {}, {} seconds in".format(x, sec), file=stderr)

def main2():
    threadPool = {} 
    stopProcessing = False
    threadKey = 1
    is_complete = os.environ['IS_COMPLETE']

    thread = threading.Thread(target = resetTest, args=(threadKey, ))
    thread.start()
    threadPool[threadKey] = thread
    threadKey = threadKey+1 
    
    print(threadPool, file=stderr)

    while threadPool:
        print(gyro.angle())
        is_complete = int(os.environ['IS_COMPLETE'])
        if is_complete != 0: 
            del threadPool[is_complete]
            is_complete = 0
            os.environ['IS_COMPLETE'] = str(is_complete)
            print("deleted thread", file=stderr)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
while True:
    if Button.CENTER in ev3.buttons.pressed():
        break
# version 1 for testing calibration

a = gyro.angle()
time.sleep(5)
b = gyro.angle()
print("5 sec apart readings: {} and {}".format(a,b))
main()
'''
# version 2 for testing reset 
main2()
s=time.time()
print(s)
while True:
    print(gyro.angle())
    if time.time() > s+2:
        break
print(time.time())
time.sleep(2)
print("last {}".format(gyro.angle()))
'''
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
time.sleep(2)
print(gyro.angle())