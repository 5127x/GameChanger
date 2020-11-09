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


def motor_onForSeconds(stop, threadKey, motor, speed, seconds):
    print("In motor_onForSeconds", file=stderr)

    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    # turn motor on for a number of seconds
    start_time = time.time()
    motor.run(speed=speed)# turn the motor on forever
    while time.time() < start_time + seconds: # while the current time is smaller than the number of seconds
        if stop():
            break
    #Once completed turn the motor off
    #robot.stop()
    motor.stop()
    print('Leaving Motor_onForSeconds', file=stderr)

    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
#stopProcessing=False
#Motor_onForSeconds(lambda:stopProcessing, motor=mediumMotor, speed=30, seconds=3)