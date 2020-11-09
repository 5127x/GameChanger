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

# follow a black line until the opposite sensor sees another line
def blackline_to_line(stop, threadKey, speed, sensor, lineSide, correction):
    # log the function starting 
    print("In blackline_to_line", file= stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    # RLI it should be reading if following the line
    target_RLI = 40

    # saves the current RLI for each sensor 
    right_RLI = colourRight.reflection()
    left_RLI = colourLeft.reflection()

    # if using the right sensor 
    if sensor == "RIGHT": 
        # if following the left side of the line
        if lineSide == "LEFT":
            # loop
            while True:
                # read the current RLI values
                right_RLI = colourRight.reflection()
                left_RLI = colourLeft.reflection()
                
                # check if there is a black line
                if left_RLI <= 15:
                    break

                # calulate the error
                error = right_RLI - target_RLI
                # calculate the needed steering to compensate
                steering = 0
                steering = error * 0.5

                # the robot drives forward 
                robot.drive(speed=speed, turn_rate = steering)
                
                # check if the 'stopProcessing' flag has been raised
                if stop():
                    break

        # if following the right side of the line
        elif lineSide == "RIGHT":
            # loop
            while True:
                # read the current RLI values
                right_RLI = colourRight.reflection()
                left_RLI = colourLeft.reflection()
                
                # check if there is a black line
                if left_RLI <= 15:
                    break

                # calculate the error
                error = target_RLI - right_RLI
                # calculate the needed steering to compensate
                steering = 0
                steering = error * 0.5

                # the robot drives forward
                robot.drive(speed=speed, turn_rate = steering)
                
                # check if the 'stopProcessing' flag has been raised 
                if stop():
                    break
    
    # if using the left sensor 
    elif sensor == "LEFT":
        # if following the right side of the line
        if lineSide == "RIGHT":
            # loop
            while True:
                # read the current RLI values
                right_RLI = colourRight.reflection()
                left_RLI = colourLeft.reflection()

                # check if there is a black line 
                if right_RLI <= 15:
                    break

                # calculate the error 
                error = target_RLI - right_RLI 
                # calculate the needed steering to compensate
                steering = 0
                steering = error * 0.5
               
                # the robot drives forward
                robot.drive(speed=speed, turn_rate = steering)
                
                # check if the 'stopProcessing' flag has been raised 
                if stop():
                    break

        # if following the left side of the line
        elif lineSide == "LEFT":
            # loop
            while True:
                # read the current RLI values
                right_RLI = colourRight.reflection()
                left_RLI = colourLeft.reflection()

                # check if there is a black line 
                if right_RLI <= 15:
                    break

                # calculate the error
                error = left_RLI - target_RLI 
                # calculate the needed steering to compensate
                steering = 0
                steering = error * 0.5
     
                # the robot drives forward 
                robot.drive(speed=speed, turn_rate = steering)
                
                # check if the 'stopProcessing' flag has been raised
                if stop():
                     break

    # stop the robot 
    robot.stop()

    # log leaving the function
    print("Leaving blackline_to_line", file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

#stopProcessing = False
#blackline_to_line(lambda: stopProcessing, 0, speed = 150, sensor = 'RIGHT', lineSide = 'RIGHT', correction = 0.8)