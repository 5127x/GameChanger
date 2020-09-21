#!/usr/bin/env pybricks-micropython
# - Micropython -
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor, GyroSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from sys import stderr
import time

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

#- - - - - - - - - - - - - - - - - - 

def Steering_seconds(stop, speed, seconds, steering): 
    print("In Steering_seconds", file=stderr)
    start_time = time.time()
    robot.drive(steering=steering, speed=speed)

    while time.time() < start_time + seconds:
        if stop():
            break
    robot.drive.off()
    print('Leaving Steering_seconds', file=stderr)

#stopProcessing=False
#Steering_seconds(lambda:stopProcessing, speed=30, seconds=3, steering=0)