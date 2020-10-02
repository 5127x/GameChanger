#!/usr/bin/env pybricks-micropython
# - Micropython -
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor, GyroSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
import os
from sys import stderr

largeMotor_Right = Motor(Port.B)
largeMotor_Left = Motor(Port.C)
panel = Motor(Port.D)

gyro = GyroSensor(Port.S1)
colourRight = ColorSensor(Port.S2)
colourLeft = ColorSensor(Port.S3)
colourkey = ColorSensor(Port.S4)


ev3 = EV3Brick()
robot = DriveBase(largeMotor_Left, largeMotor_Right, wheel_diameter=62, axle_track=104)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
import time
#- - - - - - - - - - - - - - - - - - 

def reset_gyro(threadKey):
    # calibrate the gyro by changing modes
    print("In Reset_gyro", file=stderr)

    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    time.sleep(0.5)
    gyro.reset_angle(0)
    #gyro.mode = 'GYRO-RATE'
    #gyro.mode = 'GYRO-ANG'
    time.sleep(0.5)
    current_gyro_reading = gyro.angle()
    print(current_gyro_reading, file = stderr)
    print('Leaving Reset_gyro', file=stderr)

    #tells framework the function is completed 
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)