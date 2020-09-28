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
import time
from sys import stderr
import os

# import the functions 
from Functions_Completed.blackline_rotations import blackline_rotations
from Functions_Completed.blackline_to_line import blackline_to_line
from Functions_Completed.do_nothing import do_nothing
from Functions_Completed.gyro_current import gyro_current
from Functions_Completed.gyro_target_to_line import gyro_target_to_line
from Functions_Completed.gyro_target import gyro_target
from Functions_Completed.gyro_turning import gyro_turning
from Functions_Completed.motor_onForRotations import motor_onForRotations
from Functions_Completed.off import off
from Functions_Completed.reset_gyro import reset_gyro
from Functions_Completed.steering_rotations import steering_rotations
from Functions_Completed.steering_seconds import steering_seconds
from Functions_Completed.waiting import waiting


# define the different sensors, motors and motor blocks
extention = Motor(Port.A)
largeMotor_Right = Motor(Port.B)
largeMotor_Left = Motor(Port.C)
panel = Motor(Port.D)

gyro = GyroSensor(Port.S1)
colourRight = ColorSensor(Port.S2)
colourLeft = ColorSensor(Port.S3)
colourkey = ColorSensor(Port.S4)


# launch actions using threads
def launchStep(stop, threadKey, action):
    # compare the 'name' to the functions and start a thread with the matching function
    # return the thread to be added to the threadPool
    name = action["step"]

    ''' 
   if name == '': # (list of variables)
        print(name, file=stderr)
        thread = threading.Thread(target=, args=(stop, threadKey, variables))
        thread.start()
        return thread
    
    '''
    
    if name == 'blackline_rotations':# (stop, speed, rotations, sensor, lineSide, correction)
        print("Starting BlackLine_rotations", file=stderr)
        speed = float(action['speed'])
        rotations = float(action['rotations'])
        sensor = action['sensor']
        lineSide = action['lineSide']
        correction = float(action['correction'])
        thread = threading.Thread(target = blackline_rotations, args=(stop, speed, rotations, sensor, lineSide, correction))
        thread.start()
        return thread

    if name == 'blackline_to_line': #stop, speed, sensor, lineSide, correction
        print("Starting blackline_to_line", file = stderr)
        speed = float(action['speed'])
        sensor = action['sensor']
        lineSide = action['lineSide']
        correction = float(action['correction'])
        thread = threading.Thread(target = blackline_to_line, args=(stop, speed, sensor, lineSide, correction))
        thread.start()
        return thread

    if name == 'do_nothing': # (stop)
        print("do_nothing", file= stderr)
        thread = threading.Thread(target=Do_nothing, args=(stop,))
        thread.start()
        return thread

    if name == 'gyro_current': # (stop, speed, rotations)
        print("Starting gyro_current", file=stderr)
        speed = float(action['speed'])
        rotations = float(action['rotations'])
        thread = threading.Thread(target=gyro_current, args=(stop, speed, rotations))
        thread.start()
        return thread

    if name == 'gyro_target_to_line': # (stop, speed, rotations, target, whiteOrBlack)
        print("Starting gyro_target_to_line", file=stderr)
        speed = float(action['speed'])
        rotations = float(action['rotations'])
        target = float(action[target])
        whiteOrBlack = action['whiteOrBlack']
        thread = threading.Thread(target=gyro_target_to_line, args=(stop, speed, rotations, target, whiteOrBlack))
        thread.start()
        return thread

    if name == 'gyro_target': # (stop, speed, rotations, target)
        print("Starting gyro_target", file=stderr)
        speed = float(action['speed'])
        rotations = float(action['rotations'])
        target = float(action['target'])
        thread = threading.Thread(target=gyro_target, args=(stop, speed, rotations, target))
        thread.start()
        return thread

    if name == 'gyro_turning': # (stop, speed, degrees)
        print("Starting gyro_turning", file=stderr)
        speed = float(action['speed'])
        degrees = float(action['degrees'])
        thread = threading.Thread(target = gyro_turning, args=(stop, speed, degrees))
        thread.start()
        return thread

    if name == 'motor_onForRotations': # (stop, motor, speed, rotations, gearRatio)
        print("Starting Motor_onForRotations", file=stderr)
        motor = action.get('motor')
        speed = float(action['speed'])
        rotations = float(action['rotations'])
        gearRatio = float(action['gearRatio'])
        if (motor == "largeMotor_Left"):
            motorToUse = largeMotor_Left
        if (motor == "largeMotor_Right"):
            motorToUse = largeMotor_Right
        if (motor == "panel"):
            motorToUse = panel
        thread = threading.Thread(target=motor_onForRotations, args=(stop, motorToUse, speed, rotations, gearRatio))
        thread.start()
        return thread

    if name == 'off': # ()
        print("Motors off", file=stderr)
        thread = threading.Thread(target=off)
        thread.start()
        return thread


    if name == 'reset_gyro': # ()
        print("Starting Reset_gyro", file=stderr)
        thread = threading.Thread(target=reset_gyro)
        thread.start()
        return thread

    if name == 'steering_rotations': # (stop, speed, rotations, steering)
        print("Starting Steering_rotations", file=stderr)
        speed = float(action['speed'])
        rotations = float(action['rotations'])
        steering = float(action['steering'])

        thread = threading.Thread(target=steering_rotations, args=(stop, speed, rotations, steering))
        thread.start()
        return thread

    if name == 'steering_seconds': # (stop, speed, seconds, steering)
        print("Starting Steering_seconds", file=stderr)
        speed = float(action[speed])
        seconds = float(action['seconds'])
        steering = float(action['steering'])
        thread = threading.Thread(target=Steering_seconds, args= (stop, speed, steering))
        thread.start()
        return thread

    if name == 'waiting': # (stop, seconds) 
        print("Starting waiting", file=stderr)
        seconds = float(action['seconds'])
        thread = threading.Thread(target=waiting, args=(stop, seconds))
        thread.start()
        return thread



is_complete = 0
os.environ['IS_COMPLETE'] = str(is_complete)
# main section of the program
def main():
    # create dictionaries and variables
    threadPool = {}
    stopProcessing = False
    threadKey = 1
    is_complete = os.environ['IS_COMPLETE']
    
    
    # collect the raw rgb light values from colourAttachment and the overall XML file
    with open('Run_1.json') as f:
        parsed = ujson.load(f)
        steps = parsed["steps"]
        # run each step individually unless they are run in parallel
        for step in steps:
            action = step["step"]
            print(action, file=stderr)
            print(step, file=stderr)
            # loop through actions that should be run in parallel
            if action == 'launchInParallel':
                subSteps = step["subSteps"]
                for subStep in subSteps:
                    print('substep {}'.format(subStep))
                    thread = launchStep(lambda:stopProcessing, threadKey, subStep)
                    threadPool[threadKey] = thread
                    threadKey = threadKey+1        
            else:
                #print('launch thread', file=stderr)
                thread = launchStep(lambda:stopProcessing, threadKey, step)
                #print(thread, file=stderr)
                threadPool[threadKey] = thread
                threadKey = threadKey+1        
            while not stopProcessing:
                # if there are no threads running start the next action
                if not threadPool:
                    break
                # remove any completed threads from the pool
                is_complete = int(os.environ['IS_COMPLETE'])
                if is_complete != 0: 
                    del threadPool[is_complete]
                    is_complete = 0
                    os.environ['IS_COMPLETE'] = str(is_complete)
                    print("deleted thread", file=stderr)

                    print("threadpool {}".format(threadPool), file=stderr)
                
            # if the 'stopProcessing' flag has been set then finish the whole loop
            if stopProcessing:
                off()
                break
  

main()