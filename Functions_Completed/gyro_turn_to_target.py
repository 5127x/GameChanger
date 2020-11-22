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

# 
def gyro_turn_to_target(stop, threadKey, speed, degrees):
    # log the function starting s
    print("In gyro_turn_to_target", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    # read the current degrees heading 
    current_gyro_reading = gyro.angle()
    
    # if facing to the left of the target
    if current_gyro_reading < degrees:
        # start turning the robot 
        largeMotor_Left.run(speed=speed)
        largeMotor_Right.run(speed=-speed)

        # loop until facing the correct angle 
        while current_gyro_reading < degrees:
            #print(current_gyro_reading, file=stderr)
            # read the current degress heading 
            current_gyro_reading = gyro.angle()

            # check if the robot has turned far enough
            if current_gyro_reading >= degrees:
                break

            # check if the 'stopProcessing' flag has been raised 
            if stop():
                break

    # if facing to the right of the target 
    elif current_gyro_reading > degrees:
        # start turning the robot 
        largeMotor_Left.run(speed=-speed)
        largeMotor_Right.run(speed=speed)

        # loop until the robot has turned far enough 
        while current_gyro_reading > degrees:
            #print(current_gyro_reading, file=stderr)
            # read the current degrees heading                
            current_gyro_reading = gyro.angle()

            # check if the robot had turned far enough 
            if current_gyro_reading <= degrees:
                break

            # check if the 'stopProcessing' flag has been raised 
            if stop():
                break

    # stop the robot 
    robot.stop()

    # log leaving the function
    print("Leaving gyro_turn_to_target", file=stderr)   
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)   

    #print("Current Gyro: {}".format (float(current_gyro_reading)), file=stderr)
