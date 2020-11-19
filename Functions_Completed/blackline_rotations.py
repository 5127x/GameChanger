#!/usr/bin/env pybricks-micropython
# - Micropython -
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor, GyroSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
# basic imports 
from sys import stderr
import time 
import os
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# define the motors, sensors and the brick
largeMotor_Right = Motor(Port.B)
largeMotor_Left = Motor(Port.C)
panel = Motor(Port.D)

gyro = GyroSensor(Port.S4)
colourRight = ColorSensor(Port.S2)
colourLeft = ColorSensor(Port.S3)
colourkey = ColorSensor(Port.S1)

ev3 = EV3Brick()
robot = DriveBase(largeMotor_Left, largeMotor_Right, wheel_diameter=62, axle_track=104)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# follow a black line for a set number of rotations 
def blackline_rotations(stop, threadKey, speed, rotations, sensor, lineSide,correction):
    # log the function starting 
    print("In blackline_rotations", file=stderr)
    
    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    # adjust rotations to be in degrees
    rotations = rotations*360
    # read the current motor positions 
    currentDegrees_left = largeMotor_Left.angle()
    currentDegrees_right = largeMotor_Right.angle()

    # create 'target_rotations' for how far the robot should drive in degrees
    target_left = currentDegrees_left + rotations
    target_right = currentDegrees_right + rotations
    
    # read the current RLI for each sensor 
    right_RLI = colourRight.reflection()
    left_RLI = colourLeft.reflection()
    
    # set the variables needed
    target_RLI = 22
    steering = 0

    # if using the right sensor 
    if sensor == "RIGHT": 
        # if following the left side of the line
        if lineSide == "LEFT": 
            # loop until the robot had driven far enough
            while currentDegrees_left < target_left: 
                # read the current motor positions and current RLI values
                currentDegrees_left = largeMotor_Left.angle()
                right_RLI = colourRight.reflection()
                
                # calulate the error
                error = right_RLI - target_RLI
                # calculate the needed steering to compensate
                steering = error * correction

                # the robot drives forward
                robot.drive(speed=speed, turn_rate = steering)
                
                # check if the 'stop_processing' flag has been raised
                if stop():
                    break
                
                # wait a little before the next repetition
                time.sleep(0.001)
                
        # if following the right side of the line
        elif lineSide == "RIGHT":
            # loop until the robot had driven far enough
            while currentDegrees_left < target_left and currentDegrees_right < target_right:
                # read the current motor positions and the current RLI values 
                currentDegrees_left = largeMotor_Left.angle()
                currentDegrees_right = largeMotor_Right.angle()
                right_RLI = colourRight.reflection()
                
                # calculate the error
                error = target_RLI - right_RLI
                # calculate the needed steering to compensate
                steering = error * correction

                # the robot drives forward
                robot.drive(speed=speed, turn_rate = steering)
                
                # check if the 'stopProcessing' flag has been raised
                if stop():
                    break

                # wait a little before the next repetition
                time.sleep(0.001)
    
    # if using the left sensor 
    elif sensor == "LEFT":
        # if following the right side of the line
        if lineSide == "RIGHT":
            # loop until the robot has driven far enough
            while currentDegrees_left < target_left and currentDegrees_right < target_right:
                # saves the current motor positions and the current RLI values 
                currentDegrees_left = largeMotor_Left.angle()
                currentDegrees_right = largeMotor_Right.angle()
                left_RLI = colourLeft.reflection()
                
                # calculate the error 
                error = target_RLI - right_RLI 
                # calculate the needed steering to compensate
                steering = error * correction
               
                # the robot drives forward
                robot.drive(speed=speed, turn_rate = steering)
                
                # check if the 'stopProcessing' flag has been raised
                if stop():
                    break

                # wait a little before the next repetition
                time.sleep(0.001)

        # if following the left side of the line
        elif lineSide == "LEFT":
            # loop until the robot has driven far enough
            while currentDegrees_left < target_left and currentDegrees_right < target_right:
                # saves the current motor positions and the current RLI values 
                currentDegrees_left = largeMotor_Left.angle()
                currentDegrees_right = largeMotor_Right.angle()
                left_RLI = colourLeft.reflection()
                
                # calculate the error
                error = left_RLI - target_RLI 
                # calculate the steering needed to compensate 
                steering = error * correction

                # the robot drives forward
                robot.drive(speed=speed, turn_rate = steering)
                
                # check if the 'stopProcessing' flag has been raised 
                if stop():
                    break

                # wait a little before the next repetition
                time.sleep(0.001)

    # stop the robot 
    robot.stop()

    # log leaving the function
    print("Leaving blackLine_rotations", file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

#stopProcessing = False
#blackline_rotations(lambda:stopProcessing, 0, speed = 150, rotations = 2, sensor = 'RIGHT', lineSide = 'RIGHT', correction = 0.8)