#!/usr/bin/env pybricks-micropython
# - Micropython -
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor, GyroSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile
# basic import s
import os
import time
from sys import stderr
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# define motors, sensor and the brick
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

def reset_gyro_2(stop, threadKey):
    # log the function starting 
    print("In recalibrate_gyro", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    while True:
        gyro.reset_angle(0)

        gyro = GyroSensor(Port.S4)
        loop_count = 0
        if int(loop_count) < 6:
            prev_gyro_reading = gyro.angle()
            time.sleep(0.3)
            current_gyro_reading = gyro.angle()
            print(current_gyro_reading)
            loop_count = loop_count + 1


        if current_gyro_reading == prev_gyro_reading:
            gyro.angle()
            gyro.speed()
            break


    print("finished reset gyro 2")
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)