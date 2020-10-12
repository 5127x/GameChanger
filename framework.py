#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick as ev3
from pybricks.ev3devices import ColorSensor, GyroSensor #, MediumMotor, LargeMotor (nned to find how to actually do this)
from pybricks.parameters import Port

import ujson
import threading
import time
from sys import stderr
import os

# import the functions 
''' # will be updated list soon
from program import function

from functions.Do_nothing import Do_nothing
from functions.off import off
from functions.Delay_seconds import Delay_seconds

from functions.Motor_onForRotations import Motor_onForRotations
from functions.Motor_onForSeconds import Motor_onForSeconds
from functions.Steering_rotations import Steering_rotations
from functions.Steering_seconds import Steering_seconds
from functions.Tank_rotations import Tank_rotations
from functions.Tank_seconds import Tank_seconds

from functions.Reset_gyro import Reset_gyroo
from functions.StraightGyro_target import StraightGyro_target
from functions.StraightGyro_current import StraightGyro_current 
from functions.StraightGyro_target_toLine import StraightGyro_target_toLine
from functions.StraightGyro_current_toLine import StraightGyro_current_toLine
from functions.StraightGyro_target_colourStop import StraightGyro_target_colourStop
from functions.Turn_degrees import Turn_degrees
from functions.Turn_from_start_position import Turn_from_start_position

from functions.BlackLine_rotations import BlackLine_rotations
from functions.squareOnLine import squareOnLine
from functions.squareOnLineWhite import squareOnLineWhite
'''
# define the different sensors, motors and motor blocks
'''colourAttachment = ColorSensor(Port.S4)
colourRight = ColorSensor(Port.S2)
colourLeft = ColorSensor(Port.S3)
gyro = GyroSensor(Port.S1)
largeMotor_Left= LargeMotor(Port.B)
largeMotor_Right= LargeMotor(Port.C)
mediumMotor = MediumMotor(Port.D)'''

''' # dont know what the new python version is 
steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C) 
tank_block = MoveTank(OUTPUT_B, OUTPUT_C)
'''

# check if the key has been removed
def isKeyTaken(rProgram, gProgram, bProgram): 
    # return True if the key was removed and stop the motors 
    rbgA = colourAttachment.raw
    # compare the current values to the values shown when the key is inserted   
    # (rgb values are 50, 62, 57 when the slot is empty)
    return abs(rbgA[0] - rProgram) > 12 and abs(rbgA[1] - gProgram) > 12 and abs(rbgA[2] - bProgram) > 12 #returns which run to run

# calibrate the colourAttachment values for the different keys
def colourAttachment_values(): 
    stop = False
    # set a larger font 
    os.system('setfont Lat15-TerminusBold14') # os.system('setfont Lat15-TerminusBold32x16')  

    # print instructions and collect the rgb values for each key
    # NOW ON SCALE OF 1-100 INSTEAD OF 1-255
    print('Insert red', file=stderr)
    print('Insert red')
    button.wait_for_pressed(['enter'])
    red = colourAttachment.rgb()
    print('Next.')

    print('Insert green', file=stderr)
    print('Insert green')
    button.wait_for_pressed(['enter'])
    green = colourAttachment.rgb()
    print('Next.')

    print('Insert white', file=stderr)
    print('Insert white')
    button.wait_for_pressed(['enter'])
    white = colourAttachment.rgb()
    print('Next.')

    print('Insert black', file=stderr)
    print('Insert black')
    button.wait_for_pressed(['enter'])
    black = colourAttachment.rgb()
    print('Next.')

    print('Insert yellow', file=stderr)
    print('Insert yellow')
    button.wait_for_pressed(['enter'])
    yellow = colourAttachment.rgb()
    print('Next.')

    print('Insert blue', file=stderr)
    print('Insert blue')
    button.wait_for_pressed(['enter'])
    blue = colourAttachment.rgb()
    print('Done! (press enter)')
    button.wait_for_pressed(['enter'])

    # return the values for the different keys
    attachment_values = [red, green, white, black, yellow, blue]
    return attachment_values

# launch actions using threads
def launchStep(stop, action):
    # compare the 'name' to the functions and start a thread with the matching function
    # return the thread to be added to the threadPool
    name = action["step"]

    #.......

is_complete = 0
os.environ['IS_COMPLETE'] = str(is_complete)
# main section of the program
def main():
    # create dictionaries and variables
    threadPool = {}
    stopProcessing = False
    threadKey = 1
    attachment_values = colourAttachment_values()
    # open and read the overall XML file 
    with open('overall_programming.json') as f:
        parsed = ujson.load(f)
        programsList = parsed["programs"]
    
        while True:
            # reset stopProcessing each repetition
            stopProcessing = False
            # collect the raw rgb light values from colourAttachment and the overall XML file
            rgb = colourAttachment.raw
            
            # FUCKING FIX THIS 
            for x in programsList:
                program = programsList[x]
                programName = program["name"]
                colourValue = int(program["colourValue"])
                
                # use the calibrated values in comparison 
                colourProgram = attachment_values[colourValue]
                rProgram = colourProgram[0]
                gProgram = colourProgram[1]
                bProgram = colourProgram[2]
                rColourSensor = rgb[0]
                gColourSensor = rgb[1]
                bColourSensor = rgb[2]
                # compare the sets of values
                # if the values match, run the corresponding program
                if abs(rColourSensor - rProgram) < 12 and abs(gColourSensor - gProgram) < 12 and abs(bColourSensor - bProgram) < 12:
                    mediumMotor.reset 

                    # read the relevant program XML
                    fileName = program["fileName"]
                    print(fileName,file=stderr)
                    with open(FileName) as f:
                        parsed = ujson.load(f)
                        steps = parsed[""]
                        
                        # run each step individually unless they are run in parallel
                        for step in steps:
                            action = step["step"]
                            print ('{} {}'.format(action, step), file = stderr)
                            # loop through actions that should be run in parallel
                            if action == 'launchInParallel':
                                subSteps = step["subSteps"]
                                for subStep in subSteps:
                                    print('subStep {}'.format(subStep))
                                    thread = launchStep(lambda:stopProcessing, threadKey, subStep)
                                    threadPool[threadKey] = thread
                                    threadKey = threadKey+1  
                            # run each action that isn't run in parrallel idividually
                            else:
                                thread = launchStep(lambda:stopProcessing, threadKey, step)
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
                                    print('')
                                
                                # if the robot has been lifted or the key removed then stop everything
                                if isKeyTaken(rProgram, gProgram, bProgram):
                                    stopProcessing = True
                                    break

                            # if the 'stopProcessing' flag has been set then finish the whole loop
                            if stopProcessing:
                                off()
                                break

main()