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

gyro = GyroSensor(Port.S1)
colourRight = ColorSensor(Port.S2)
colourLeft = ColorSensor(Port.S3)
colourkey = ColorSensor(Port.S4)

ev3 = EV3Brick()
robot = DriveBase(largeMotor_Left, largeMotor_Right, wheel_diameter=62, axle_track=104)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# use the gyro to drive in a straight line facing the direction it currently faces until the sensor sees a line
def gyro_current_to_line(stop, threadKey, speed, sensor, correction):
    # log the function starting 
    print("In gyro_current_to_line", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    # create the target degrees
    target = gyro.angle()
    # read the current degrees heading and the current RLI value
    current_gyro_reading = target
    if sensor == "RIGHT":
        RLI = colourRight.reflection()
    elif sensor == "LEFT":
        RLI = colourLeft.reflection()

    # loop 
    while True:  
        # read the current degrees heading and the RLI value 
        current_gyro_reading=gyro.angle()
        if sensor == "RIGHT":
            RLI = colourRight.reflection()
        elif sensor == "LEFT":
            RLI = colourLeft.reflection()
        
        # if facing to the right of the target
        if current_gyro_reading > target:
            # calculate the error 
            error = target - current_gyro_reading 
            # calculate the needed steering to compensate
            steering = error * correction 

            # the robot drives forward 
            robot.drive(turn_rate = steering , speed = speed) 

        # if facing to the left of the target
        if current_gyro_reading < target:
            # calculate the error 
            error = target - current_gyro_reading
            # calculated the needed steering to compensate 
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
    print('Leaving gyro_current_to_line', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

#stopProcessing=False
#gyro_current_to_line(lambda:stopProcessing, 0, speed = 150, sensor = 'RIGHT', correction = 0.5)
