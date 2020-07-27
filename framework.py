#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick as ev3
from pybricks.ev3devices import ColorSensor, GyroSensor, MediumMotor, LargeMotor
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
'''
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
colourAttachment = ColorSensor(Port.S4)
colourRight = ColorSensor(Port.S2)
colourLeft = ColorSensor(Port.S3)
gyro = GyroSensor(Port.S1)
largeMotor_Left= LargeMotor(Port.B)
largeMotor_Right= LargeMotor(Port.C)
mediumMotor = MediumMotor(Port.D)

'''
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
    print('Insert red', file=stderr)
    print('Insert red')
    button.wait_for_pressed(['enter'])
    red = colourAttachment.raw 
    print('Next.')

    print('Insert green', file=stderr)
    print('Insert green')
    button.wait_for_pressed(['enter'])
    green = colourAttachment.raw
    print('Next.')

    print('Insert white', file=stderr)
    print('Insert white')
    button.wait_for_pressed(['enter'])
    white = colourAttachment.raw
    print('Next.')

    print('Insert black', file=stderr)
    print('Insert black')
    button.wait_for_pressed(['enter'])
    black = colourAttachment.raw
    print('Next.')

    print('Insert yellow', file=stderr)
    print('Insert yellow')
    button.wait_for_pressed(['enter'])
    yellow = colourAttachment.raw
    print('Next.')

    print('Insert blue', file=stderr)
    print('Insert blue')
    button.wait_for_pressed(['enter'])
    blue = colourAttachment.raw
    print('Done!')
    button.wait_for_pressed(['enter'])

    # return the values for the different keys
    attachment_values = [red, green, white, black, yellow, blue]
    return attachment_values

# launch actions using threads
def launchStep(stop, action):
    # compare the 'name' to the functions and start a thread with the matching function
    # return the thread to be added to the threadPool
    name = action["step"]

    if name == '': # (list of variables)
        print(name, file=stderr)
        thread = threading.Thread(target=, args=(stop, variables))
        thread.start()
        return thread

    '''
    if name == 'Do_nothing': # (stop)
        print("Do_nothing", file= stderr)
        thread = threading.Thread(target=Do_nothing, args=(stop,))
        thread.start()
        return thread

    if name == 'off': # ()
        print("Motors off", file=stderr)
        thread = threading.Thread(target=off)
        thread.start()
        return thread

    if name == 'Delay_seconds': # (stop, seconds) 
        print("Starting Delay_seconds", file=stderr)
        seconds = float(action.get('seconds'))
        thread = threading.Thread(target=Delay_seconds, args=(stop, seconds))
        thread.start()
        return thread

    if name == 'Motor_onForRotations': # (stop, motor, speed, rotations, gearRatio)
        print("Starting Motor_onForRotations", file=stderr)
        motor = action.get('motor')
        speed = float(action.get('speed'))
        rotations = float(action.get('rotations'))
        gearRatio = float(action.get('gearRatio'))
        if (motor == "largeMotor_Left"):
            motorToUse = largeMotor_Left
        if (motor == "largeMotor_Right"):
            motorToUse = largeMotor_Right
        if (motor == "mediumMotor"):
            motorToUse = mediumMotor
        thread = threading.Thread(target=Motor_onForRotations, args=(stop, motorToUse, speed, rotations, gearRatio))
        thread.start()
        return thread

    if name == 'Motor_onForSeconds': # (stop, motor, speed, seconds)
        print("Starting Motor_onForSeconds", file=stderr)
        motor = action.get('motor')
        speed = float(action.get('speed'))
        seconds = float(action.get('seconds'))
        if (motor == "largeMotor_Left"):
            motorToUse = largeMotor_Left
        if (motor == "largeMotor_Right"):
            motorToUse = largeMotor_Right
        if (motor == "mediumMotor"):
            motorToUse = mediumMotor
        thread = threading.Thread(target=Motor_onForSeconds,args=(stop, motorToUse, speed, seconds))
        thread.start()
        return thread
    
    if name == 'Steering_rotations': # (stop, speed, rotations, steering)
        print("Starting Steering_rotations", file=stderr)
        speed = float(action.get('speed'))
        rotations = float(action.get('rotations'))
        steering = float(action.get('steering'))
        brake = bool(action.get('brake'))
        thread = threading.Thread(target=Steering_rotations, args=(stop, speed, rotations, steering))
        thread.start()
        return thread
    
    if name == 'Steering_seconds': # (stop, speed, seconds, steering)
        print("Starting Steering_seconds", file=stderr)
        speed = float(action.get('speed'))
        seconds = float(action.get('seconds'))
        steering = float(action.get('steering'))
        thread = threading.Thread(target=Steering_seconds, args= (stop, speed, steering))
        thread.start()
        return thread

    if name == 'Tank_rotations': # (stop, left_speed, right_speed, rotations)
        print("Starting Tank_rotations", file=stderr)
        left_speed = float(action.get('left_speed'))
        right_speed = float(action.get('right_speed'))
        rotations = float(action.get('rotations'))
        thread = threading.Thread(target = Tank_rotations, args=(stop, left_speed, right_speed, rotations))
        thread.start()
        return thread

    if name == 'Tank_seconds': # (stop, left_speed, right_speed, seconds)
        print("Starting Tank_seconds", file=stderr)
        left_speed = float(action.get('left_speed'))
        right_speed = float(action.get('right_speed'))
        seconds = float(action.get('seconds'))
        thread = threading.Thread(target = Tank_seconds, args=(stop, left_speed, right_speed, seconds))
        thread.start()
        return thread
    
    if name == 'Reset_gyro': # ()
        print("Starting Reset_gyro", file=stderr)
        thread = threading.Thread(target=Reset_gyro)
        thread.start()
        return thread

    if name == 'StraightGyro_target': # (stop, speed, rotations, target)
        print("Starting StraightGyro_target", file=stderr)
        speed = float(action.get('speed'))
        rotations = float(action.get('rotations'))
        target = float(action.get('target'))
        thread = threading.Thread(target=StraightGyro_target, args=(stop, speed, rotations, target))
        thread.start()
        return thread

    if name == 'StraightGyro_target_colourStop': # (stop, speed, target, sensor, value)
        print("Starting StraightGyro_target_colourStop", file=stderr)
        speed = float(action.get('speed'))
        target = float(action.get('target'))
        sensor = action.get('sensor')
        value = float(action.get('value'))
        thread = threading.Thread(target=StraightGyro_target_colourStop, args=(stop, speed, target, sensor, value))
        thread.start()
        return thread

    if name == 'StraightGyro_current': # (stop, speed, rotations)
        print("Starting StraightGyro_current", file=stderr)
        speed = float(action.get('speed'))
        rotations = float(action.get('rotations'))
        thread = threading.Thread(target=StraightGyro_current, args=(stop, speed, rotations))
        thread.start()
        return thread

    if name == 'StraightGyro_target_toLine': # (stop, speed, rotations, target, whiteOrBlack)
        print("Starting StraightGyro_target", file=stderr)
        speed = float(action.get('speed'))
        rotations = float(action.get('rotations'))
        target = float(action.get('target'))
        whiteOrBlack = action.get('whiteOrBlack')
        thread = threading.Thread(target=StraightGyro_target_toLine, args=(stop, speed, rotations, target, whiteOrBlack))
        thread.start()
        return thread

    if name == 'StraightGyro_current_toLine': # (stop, speed, rotations, whiteOrBlack)
        print("Starting StraightGyro_current", file=stderr)
        speed = float(action.get('speed'))
        rotations = float(action.get('rotations'))
        whiteOrBlack = action.get('whiteOrBlack')
        thread = threading.Thread(target=StraightGyro_current_toLine, args=(stop, speed, rotations, whiteOrBlack))
        thread.start()
        return thread
    
    if name == 'Turn_degrees': # (stop, speed, degrees)
        print("Starting Turn_degrees", file=stderr)
        speed = float(action.get('speed'))
        degrees = float(action.get('degrees'))
        thread = threading.Thread(target = Turn_degrees, args=(stop, speed, degrees))
        thread.start()
        return thread

    if name == 'Turn_from_start_position': # (stop, speed, degrees)
        print('Starting Turn_from_start_position', file=stderr)
        speed = float(action.get('speed'))
        degrees = float(action.get('degrees'))
        thread = threading.Thread(target = Turn_from_start_position, args=(stop, speed, degrees))
        thread.start()
        return thread


    if name == 'squareOnLine': # (stop, speed, target)
        print("Starting squareOnLine", file=stderr)
        speed = float(action.get('speed'))
        target = float(action.get('target'))
        thread = threading.Thread(target=squareOnLine, args=(stop, speed, target))
        thread.start()
        return thread
    
    if name == 'squareOnLineWhite': # (stop, speed, target)
        print("Starting squareOnLine White", file=stderr)
        speed = float(action.get('speed'))
        target = float(action.get('target'))
        thread = threading.Thread(target=squareOnLine, args=(stop, speed, target))
        thread.start()
        return thread

    if name == 'Blacklinetestinghome': # (stop, speed, correction)
        print("Blackline testing home", file=stderr)
        speed = float(action.get('speed'))
        correction = float(action.get('correction'))
        thread = threading.Thread(target = Blacklinetestinghome, args=(stop, speed, rotations, sensor, lineSide, correction))
        thread.start()
        return thread
'''


# main section of the program
def main():
    # create dictionaries and variables
    threadPool = []
    stopProcessing = False
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
            
            for x in range(0, len(programsList)):
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
                            # loop through actions that should be run in parallel
                            if action == 'launchInParallel':
                                for step in range(0, len(action)):
                                    thread = launchStep(lambda:stopProcessing, step)
                                    threadPool.append(thread)
                            # run each action that isn't run in parrallel idividually
                            else:
                                thread = launchStep(lambda:stopProcessing, step)
                                threadPool.append(thread)
#----------------------------------------------------------------------------------------------
                            while not stopProcessing:
                                # if there are no threads running start the next action
                                if not threadPool:
                                    break
                                # remove any completed threads from the pool
                                for thread in threadPool:
                                    if not thread.isAlive():
                                        threadPool.remove(thread)
                                # if the robot has been lifted or the key removed then stop everything
                                if isKeyTaken(rProgram, gProgram, bProgram):
                                    stopProcessing = True
                                    break
                            # if the 'stopProcessing' flag has been set then finish the whole loop
                            if stopProcessing:
                                off()
                                break

main()