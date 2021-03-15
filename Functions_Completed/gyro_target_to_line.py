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

# define the motors, sensors and the brick
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

# use the gyro to drive in a straight line facing the given direction until the sensor sees a line
def gyro_target_to_line(stop, threadKey, speed, sensor, target, correction):
    # log the function starting
    print("In gyro_target_to_line", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    gyro_reading_env_var = float(os.environ['gyro_reading_env_var'])
    # read the current degrees heading and the current RLI values
    current_gyro_reading = gyro.angle() - gyro_reading_env_var
    if sensor == "RIGHT":
        RLI = colourRight.reflection()
    elif sensor == "LEFT":
        RLI = colourLeft.reflection()

    # loop
    while True:
        # read the current degrees heading and the current RLI values
        current_gyro_reading=gyro.angle() - gyro_reading_env_var
        if sensor == "RIGHT":
            RLI = colourRight.reflection()
        elif sensor == "LEFT":
            RLI = colourLeft.reflection()

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

        # check if there is a black line
        if RLI <= 15:
            break

        # check if the 'stopProcessing' flag has been raised
        if stop():
            break

    # stop the robot 
    robot.stop()

    # log leaving the function 
    print('Leaving gyro_target_to_line', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

#stopProcessing=False
#StraightGyro_target(lambda:stopProcessing, 0, speed = 30, sensor = 'RIGHT', target = 0, correction = 0.8)