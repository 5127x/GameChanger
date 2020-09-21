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
from Testing_programs.RLI_testing2 import RLI_testing2

# define the different sensors, motors and motor blocks
'''colourAttachment = ColorSensor(Port.S4)
colourRight = ColorSensor(Port.S2)'''
colourLeft = ColorSensor(Port.S2) # should be S3
'''gyro = GyroSensor(Port.S1)
largeMotor_Left= LargeMotor(Port.B)
largeMotor_Right= LargeMotor(Port.C)
mediumMotor = MediumMotor(Port.D)'''

# launch actions using threads
def launchStep(stop, threadKey, action):
    # compare the 'name' to the functions and start a thread with the matching function
    # return the thread to be added to the threadPool
    name = action["step"]

    '''if name == '': # (list of variables)
        print(name, file=stderr)
        thread = threading.Thread(target=, args=(stop, threadKey, variables))
        thread.start()
        return thread'''

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
    if name == 'RLI_testing2': #(threadKey, )
        print("RLI_testing2", file=stderr)
        thread = threading.Thread(target = RLI_testing2, args=(threadKey, ))
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
    with open('testing.json') as f:
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