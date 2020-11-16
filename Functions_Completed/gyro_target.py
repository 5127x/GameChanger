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

# define motors, sensors and the brick
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

# use the gyro to drive in a straight line facing the given direction for a set number of rotations
def gyro_target(stop, threadKey, speed, rotations, target, correction):
    # log the function starting
    print("In gyro_target", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    # read the current degrees heading and the current motor positions 
    current_gyro_reading = gyro.angle()
    current_rotations = largeMotor_Left.angle() 
    # create 'target_rotations' for how far the robot should drive in degrees 
    rotations = rotations * 360
    target_rotations= current_rotations + rotations
    

    # loop until the robor has driven far enough
    while float(current_rotations) < target_rotations:
        # reading in current degrees heading and current motor positions 
        current_gyro_reading=gyro.angle()
        current_rotations = largeMotor_Left.angle()

        # if facing to the left of the target
        if current_gyro_reading < target:
            # calculate the error
            error = target - current_gyro_reading 
            # calculate the needed steering to compensate 
            steering = error * correction 

            # the robot drives forward 
            robot.drive(turn_rate = steering , speed = speed) 

        # if facing to the right of the target
        if current_gyro_reading > target:
            # calculate the error 
            error = target - current_gyro_reading 
            # calculate the needed steering to compensate 
            steering = error * correction  

            # the robot drives forward 
            robot.drive(turn_rate = steering , speed = speed)

        # if perfectly straight
        if current_gyro_reading == target:
            # the robot drives forward 
            robot.drive(turn_rate = 0 , speed = speed)

        # check if the robot has driven far enough
        if current_rotations >= target_rotations:
            break
        
        # check if the 'stopProcessing' flag is raised 
        if stop():
            break

    # stop the robot
    robot.stop()

    # log leaving the function
    print('Leaving gyro_target', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

#stopProcessing=False
#gyro_target(lambda:stopProcessing, 0, speed = 30, rotations = 3, target = 0, correction = 0.8)