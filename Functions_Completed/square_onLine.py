#!/usr/bin/env pybricks-micropython
# - Micropython -
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor, GyroSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from sys import stderr
import time
import os

largeMotor_Right = Motor(Port.B)
largeMotor_Left = Motor(Port.C)
panel = Motor(Port.D)

gyro = GyroSensor(Port.S1)
colourRight = ColorSensor(Port.S2)
colourLeft = ColorSensor(Port.S3)
colourkey = ColorSensor(Port.S4)


ev3 = EV3Brick()
robot = DriveBase(largeMotor_Left, largeMotor_Right, wheel_diameter=62, axle_track=104)
#_________________________________________________________________________________________________________________________________


def square_onLine(stop, speed, target):
    print("In squareOnLine", file=stderr)
    # setting up program
    colourLeft_RLI = 0
    colourRight_RLI = 0
    lineFound = False
    #Turning on motor
    robot.drive(turn_rate =0,speed=speed)
    while True:
        #reading in the colour sensor values (reflected light intensity)
        right_RLI = colourRight.reflection()
        left_RLI = colourLeft.reflection()
        # if the left Rli is smaller than the target/aim then turn to the right
        if left_RLI <= target:
            largeMotor_Left.on(-speed)
            largeMotor_Right.on(speed)
            lineFound = True #setting bool varisable for cancelling movment later on
            print('{} left found it'.format(colourLeft_RLI), file = stderr)

        # if the right Rli is smaller than the target/aim then turn to the left
        if right_RLI <=target:
            largeMotor_Left.on(speed)
            largeMotor_Right.on(-speed)
            lineFound = True #setting bool varisable for cancelling movment later on
            print('{} right found it'.format(colourRight_RLI), file = stderr)

        print('{} left, {} right'.format(left_RLI, right_RLI), file = stderr)
    
        if left_RLI == right_RLI and lineFound:
            break
        if stop():
            break
    robot.stop()
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)   

    print('Leaving squareOnLine', file=stderr)

#stopProcessing=False
#squareOnLine(lambda:stopProcessing, speed=30, target=100)