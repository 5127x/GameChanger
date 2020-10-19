#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick as ev3
from pybricks.ev3devices import ColorSensor, GyroSensor, Motor
from pybricks.parameters import Port
'''
from ev3dev2.motor import MoveSteering, MoveTank, MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, GyroSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.button import Button'''
import ujson
import threading
#from threading import enumerate 
'''----------
Traceback (most recent call last):
  File "/home/robot/GameChanger//thread.py", line 12, in <module>
ImportError: cannot import name enumerate
----------
Exited with error code 1.'''

import time
from sys import stderr
import os

# import the functions 
from Testing_programs.RLI_testing2 import RLI_testing2




from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port
import time
import threading
from sys import stderr 

ev3 = EV3Brick()
colourRight = ColorSensor(Port.S2)

def xyz(threadKey):
    print('sdfg', file=stderr)
    global is_complete
    x=0
    start_time = time.time()
    while time.time() < start_time + 1:
        RLI = colourRight.reflection()
        x = x+1
    print(x, file=stderr)
    is_complete = threadKey
    print(is_complete, file=stderr)

'''
is_complete = 0
def main2():
    threadPool = {} 
    stopProcessing = False
    threadKey = 1
    global is_complete
    print("RLI_testing2", file=stderr)

    thread = threading.Thread(target = xyz, args= (threadKey, ))
    thread.start()
    threadPool[threadKey] = thread

    threadKey = threadKey+1 # change position inn full framework
    
    while not stopProcessing:
        # if there are no threads running start the next action
        print(threadPool, file=stderr)
        while threadPool:
            if is_complete != 0: # doesnt return global variable properly (?) if downloaded
                del threadPool[is_complete]
                is_complete = 0
                print("deleted thread", file=stderr)
    ''' 

def xcv(threadKey):
    print('sdfg', file=stderr)

    is_complete = None
    if 'MYVAL' in os.environ:
        is_complete = os.environ['MYVAL']

    x=0
    start_time = time.time()
    while time.time() < start_time + 1:
        RLI = colourRight.reflection()
        x = x+1
    print(x, file=stderr)
    is_complete = threadKey
    print("sdfghfdgdsf {}".format(is_complete), file=stderr)



is_complete = 0
os.environ['IS_COMPLETE'] = str(is_complete)

def main2():
    threadPool = {} 
    stopProcessing = False
    threadKey = 1
    is_complete = os.environ['IS_COMPLETE']
    print("RLI_testing2", file=stderr)

    thread = threading.Thread(target = RLI_testing2, args= (threadKey, ))
    thread.start()
    threadPool[threadKey] = thread

    threadKey = threadKey+1 

    
    print(threadPool, file=stderr)
    while threadPool:
        #print("hi")
        is_complete = int(os.environ['IS_COMPLETE'])
        if is_complete != 0: 
            del threadPool[is_complete]
            is_complete = 0
            os.environ['IS_COMPLETE'] = str(is_complete)
            print("deleted thread", file=stderr)

#main1()
#main2()

def main():
    # set up threadPool 
    threadPool = []
    
    # start RLI_testing as a thread
    print("RLI_testing", file=stderr)
    threadKey = 0
    thread = threading.Thread(target=RLI_testing2, args=(threadKey, ))
    thread.start()
    # add the thread to threadPool 
    threadPool.append(thread)
 
    # while there are threads running
    print(threadPool, file=stderr)
    while threadPool:
        # remove any finished threads from threadPool
        for thread in threadPool:
            if not thread.isAlive():
                threadPool.remove(thread)
            
main()
 



# .remove(thread) works
# line 1092 of threading
''' 
https://sites.google.com/site/ev3python/learn_ev3_python/threads
https://www.programiz.com/python-programming/global-local-nonlocal-variables
'''