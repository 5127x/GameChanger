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

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#- - - - - - - - - - - - - - - - - - 

def gyro_target(stop, threadKey, speed, rotations, target, correction):
    print("In StraightGyro_target", file=stderr)

    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    current_rotations = largeMotor_Left.angle() 
    rotations = rotations * 360
    target_rotations= current_rotations + rotations
    current_gyro_reading = gyro.angle()

    # print("Current Gyro Reading: {}".format(current_gyro_reading))
    while float(current_rotations) < target_rotations:
        if stop(): 
            break
        
        #print(current_gyro_reading, file = stderr)

        # reading in current gyro and  rotations
        current_gyro_reading=gyro.angle()
        current_rotations = largeMotor_Left.angle()

        #if the gyro is smaller than the target
        if current_gyro_reading > target:
            error = target - current_gyro_reading # calculate full error by target - gyro
            steering = error * correction # 1/4 of the correction (so the robot doesn't over correct)
            robot.drive(turn_rate = -steering , speed = speed) # turn by the correctuion and doesn't over correct

        #if the gyro is larger than the target
        if current_gyro_reading < target:
            error = target - current_gyro_reading # calculate full error by target - gyro
            steering = error * correction  # 1/4 of the correction (so the robot doesn't over correct)
            robot.drive(turn_rate = steering , speed = speed) # turn by the correctuion and doesn't over correct

        #if the gyro is == to the target just go straight
        if current_gyro_reading == target:
            robot.drive(turn_rate = 0 , speed = speed)

        # if the current rotations is larger than the target then break the loop which will stop the robot
        if current_rotations >= target_rotations:
            break

        if stop():
            break

        

    robot.stop()
    print('Leaving StraightGyro_target', file=stderr)

    #tells framework the function is completed 
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

#stopProcessing=False
#StraightGyro_target(lambda:stopProcessing, speed=30, rotations=3)