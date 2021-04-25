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

gyro = GyroSensor(Port.S4)
colourRight = ColorSensor(Port.S2)
colourLeft = ColorSensor(Port.S3)
colourkey = ColorSensor(Port.S1)

ev3 = EV3Brick()
robot = DriveBase(largeMotor_Left, largeMotor_Right, wheel_diameter=62, axle_track=104)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# drive using a steering block for a set number of rotations
def steering_rotations(stop, threadKey, speed, rotations, steering):
    # log starting the function
    print("In Steering_rotations", file=stderr)

    #print("current gyro val", gyro.angle(), file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    # read the current motor positions 
    current_rotations_left = largeMotor_Left.angle() 
    current_rotations_right = largeMotor_Right.angle()

    # create 'target_rotations' for how far the robot should drive in degrees
    target_rotations = rotations * 360 
    if speed < 0:
        target_rotations_left = current_rotations_left - target_rotations
        target_rotations_right = current_rotations_right - target_rotations
    elif speed > 0:
        target_rotations_left = current_rotations_left + target_rotations
        target_rotations_right = current_rotations_right + target_rotations

    # start the robot driving 
    robot.drive(turn_rate = steering, speed= speed) # turn the robot on forever calling the parameters from above

    # if the robot is driving straight forward
    if current_rotations_left < target_rotations_left and current_rotations_right < target_rotations_right:
        # loop until the robot has driven far enough
        while current_rotations_left < target_rotations_left or current_rotations_right < target_rotations_right: 
            current_rotations_left = largeMotor_Left.angle() 
            current_rotations_right = largeMotor_Right.angle()
            # check if 'stopProcessing' flag is raised
            if stop():
                break
            # check if the robot has driven far enough
            if current_rotations_left >= target_rotations_left or current_rotations_right >= target_rotations_right:
                break
    
    # if the robot driving and turning right
    elif current_rotations_left < target_rotations_left and current_rotations_right > target_rotations_right:
        # loop until the robot has driven far enough
        while current_rotations_left < target_rotations_left or current_rotations_right > target_rotations_right: # how its done in tank onForRotations
            current_rotations_left = largeMotor_Left.angle() 
            current_rotations_right = largeMotor_Right.angle()
            # check if 'stopProcessing' flag is raised
            if stop():
                break
            # check if the robot has driven far enough
            if current_rotations_left >= target_rotations_left or current_rotations_right <= target_rotations_right:
                break
    
    # if the robot is driving and turning left 
    elif current_rotations_left > target_rotations_left and current_rotations_right < target_rotations_right:
        # loop until the robot has driven far enough
        while current_rotations_left > target_rotations_left or current_rotations_right < target_rotations_right: # how its done in tank onForRotations
            current_rotations_left = largeMotor_Left.angle() 
            current_rotations_right = largeMotor_Right.angle()
            # check if 'stopProcessing' flag is raised
            if stop():
                break
            # check if the robot has driven far enough
            if current_rotations_left <= target_rotations_left or current_rotations_right >= target_rotations_right:
                break
    
    # if the robot is driving backwards
    elif current_rotations_left > target_rotations_left and current_rotations_right > target_rotations_right:
        # loop until the robot has driven far enough
        while current_rotations_left > target_rotations_left or current_rotations_right > target_rotations_right: # how its done in tank onForRotations
            current_rotations_left = largeMotor_Left.angle() 
            current_rotations_right = largeMotor_Right.angle()
            # check if 'stopProcessing' flag is raised
            if stop():
                break
            # check if the robot has driven far enough
            if current_rotations_left <= target_rotations_left or current_rotations_right <= target_rotations_right:
                break
    
    # stop the robot 
    robot.stop()

    # log leaving the function
    print('Leaving Steering_rotations', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# drive using a steering block for a set amount of time
def steering_seconds(stop, threadKey, speed, seconds, steering): 
    # log the function starting
    print("In Steering_seconds", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    # read the current time
    start_time = time.time()
    # start the robot driving
    robot.drive(turn_rate=steering, speed=speed)

    # wait until the set amount of time has passed
    while time.time() < start_time + seconds:
        # check if 'stopProcessing' flag is raised
        if stop():
            break
    
    # stop the robot 
    robot.stop()

    # log leaving the function
    print('Leaving Steering_seconds', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#stopProcessing=False
#steering_seconds(lambda:stopProcessing, 0, speed = 200, seconds = 3, steering = 0)
#steering_rotations(lambda:stopProcessing, 0, speed = 200, rotations = 2, steering = 0)