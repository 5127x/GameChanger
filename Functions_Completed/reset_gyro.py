#!/usr/bin/env pybricks-micropython
# - Micropython -
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor, GyroSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
# basic import s
import os
import time
from sys import stderr
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# define motors, sensor and the brick
largeMotor_Right = Motor(Port.B)
largeMotor_Left = Motor(Port.C)
panel = Motor(Port.D)

gyro = GyroSensor(Port.S1)
colourRight = ColorSensor(Port.S2)
colourLeft = ColorSensor(Port.S3)
colourkey = ColorSensor(Port.S4)

ev3 = EV3Brick()
robot = DriveBase(largeMotor_Left, largeMotor_Right, wheel_diameter=62, axle_track=104)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# recalibrates the gyro before a run
def reset_gyro(stop, threadKey):
    # log the function starting 
    print("In reset_gyro", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])
    
    '''# recalibrates the gyro angle by switching between modes
    time.sleep(1)
    gyro.speed()
    gyro.angle()
    gyro.reset_angle(0)
    time.sleep(1)

    # print the current gyro reading to check for gyro creep
    current_gyro_reading = gyro.angle()
    print(current_gyro_reading, file = stderr))'''

    # loop until the gyro is reset properly 
    while True: 
        time.sleep(0.5)
        gyro.speed()
        gyro.angle()
        gyro.reset_angle(0)
        time.sleep(2)
        
        current_gyro_reading = gyro.angle()
        print(current_gyro_reading, file = stderr)

        # check if the gyro has reset properly
        if current_gyro_reading == 0:
            break
        
        # check if 'stopProcessing' flag has been raised 
        if stop:
            break

    # log leaving the function
    print('Leaving Reset_gyro', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

#reset_gyro(0)