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

gyro = GyroSensor(Port.S4)
colourRight = ColorSensor(Port.S2)
colourLeft = ColorSensor(Port.S3)
colourkey = ColorSensor(Port.S1)


ev3 = EV3Brick()
robot = DriveBase(largeMotor_Left, largeMotor_Right, wheel_diameter=62, axle_track=104)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#- - - - - - - - - - - - - - - - - - 

def gyro_turning(stop, threadKey, speed, degrees): 
    # create the target degrees
    print("In Turn_degrees", file=stderr)

    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])
    
    gyro_reading_env_var = float(os.environ['gyro_reading_env_var'])

    #read in the current gyro
    current_gyro_reading = gyro.angle() - gyro_reading_env_var
    target_degrees = current_gyro_reading + degrees

    #_____________If turning Left__________________________________
    while target_degrees > current_gyro_reading: 
        print(speed, file = stderr)

        #same concept as a tank block however bc we dont have access had to turn on both motors
        largeMotor_Right.run(speed=-speed)
        largeMotor_Left.run(speed=speed) 
        
        #print(current_gyro_reading,file=stderr)

        if target_degrees > current_gyro_reading:
            current_gyro_reading = gyro.angle() - gyro_reading_env_var
            if current_gyro_reading == target_degrees:
                break
            if stop():
                break

    #_____________If turning Right__________________________________
    while target_degrees < current_gyro_reading:
        largeMotor_Right.run(speed=speed)
        largeMotor_Left.run(speed=-speed)
        
        #print(current_gyro_reading,file=stderr)

        if target_degrees <current_gyro_reading:
            current_gyro_reading = gyro.angle()
            if current_gyro_reading == target_degrees:
                break
            if stop():
                break



    robot.stop()
    print('Leaving Turn_degrees', file= stderr)

    #tells framework the function is completed 
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

#stopProcessing=False
#Turn_degrees(lambda:stopProcessing, speed=30, degrees=90)