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

def squareOnLine(stop, speed, target):
    print("In squareOnLine", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    # setting up program
    colourLeft_RLI = 0
    colourRight_RLI = 0
    lineFound = False
    #Turning on motor
    steering_drive.on(steering=0,speed=speed)
    while True:
        #reading in the colour sensor values (reflected light intensity)
        colourLeft_RLI = colourLeft.reflection()
        colourRight_RLI = colourRight.reflection()
        # if the left Rli is smaller than the target/aim then turn to the right
        if colourLeft_RLI <= target:
            largeMotor_Left.on(-speed)
            largeMotor_Right.on(speed)
            lineFound = True #setting bool varisable for cancelling movment later on
            print('{} left found it'.format(colourLeft_RLI), file = stderr)

        # if the right Rli is smaller than the target/aim then turn to the left
        if colourRight_RLI <=target:
            largeMotor_Left.on(speed)
            largeMotor_Right.on(-speed)
            lineFound = True #setting bool varisable for cancelling movment later on
            print('{} right found it'.format(colourRight_RLI), file = stderr)

        print('{} left, {} right'.format(colourLeft_RLI, colourRight_RLI), file = stderr)
    
        if colourLeft_RLI == colourRight_RLI and lineFound:
            break
        if stop():
            break

    # stop the robot 
    robot.stop()

    # log leaving the function
    print("Leaving square_on_line", file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)


#stopProcessing=False
#squareOnLine(lambda:stopProcessing, speed=30, target=100)