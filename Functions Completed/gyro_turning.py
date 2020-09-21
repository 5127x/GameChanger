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

def Turn_degrees(stop, speed, degrees): 
    # create the target degrees
    print("In Turn_degrees", file=stderr)
    #read in the current gyro
    current_gyro_reading = gyro.angle
    target_degrees = current_gyro_reading + degrees
    if current_gyro_reading > target_degrees: # if the current reading is smaller than the target 
        tank_block(right_speed = -speed, left_speed = speed) # turn
        while current_gyro_reading > target_degrees: #while the gyro is bigger than the target rotations
            current_gyro_reading = gyro.angle
            if stop():
                break

    elif current_gyro_reading < target_degrees:  # if the current reading is larger than the target 
        tank_block(right_speed = speed, left_speed = -speed) # turn
        while current_gyro_reading < target_degrees: #while the gyro is smaller than the target rotations
            current_gyro_reading = gyro.angle
            if stop():
                break

    tank_block.off()
    print('Leaving Turn_degrees', file= stderr)

#stopProcessing=False
#Turn_degrees(lambda:stopProcessing, speed=30, degrees=90)