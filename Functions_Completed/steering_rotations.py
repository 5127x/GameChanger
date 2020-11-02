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

def steering_rotations(stop, threadKey, speed, rotations, steering):
    print("In Steering_rotations", file=stderr)

    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    current_rotations_left = largeMotor_Left.angle() # there isnt a way to read rotations
    current_rotations_right = largeMotor_Right.angle()
    target_rotations = rotations * 360 # convert to degrees bcs its simpler
    if speed < 0:
        target_rotations_left = current_rotations_left - target_rotations
        target_rotations_right = current_rotations_right - target_rotations
    elif speed > 0:
        target_rotations_left = current_rotations_left + target_rotations
        target_rotations_right = current_rotations_right + target_rotations

    robot.drive(turn_rate = steering, speed= speed) # turn the robot on forever calling the parameters from above

    if current_rotations_left < target_rotations_left and current_rotations_right < target_rotations_right:
        print("1", file=stderr)
        while current_rotations_left < target_rotations_left or current_rotations_right < target_rotations_right: # how its done in tank onForRotations
            #reading in the current rotations of the left and right motor
            current_rotations_left = largeMotor_Left.angle() 
            current_rotations_right = largeMotor_Right.angle()
            #print ("target l {} target r: {} left{} right{}".format(target_rotations_left, target_rotations_right ,current_rotations_left, current_rotations_right), file = stderr)
            if stop():
                break
            #if the current rotations of the motor on either left or right side is larger than there specific target then cancel the program or break
            if current_rotations_left >= target_rotations_left or current_rotations_right >= target_rotations_right:
                break
    # < >
    elif current_rotations_left < target_rotations_left and current_rotations_right > target_rotations_right:
        print("2", file=stderr)
        while current_rotations_left < target_rotations_left or current_rotations_right > target_rotations_right: # how its done in tank onForRotations
            current_rotations_left = largeMotor_Left.angle() 
            current_rotations_right = largeMotor_Right.angle()
            if stop():
                break
            if current_rotations_left >= target_rotations_left or current_rotations_right <= target_rotations_right:
                break
    # if left motor's current rotations is larger and the right current rotations are smaller do the code
    elif current_rotations_left > target_rotations_left and current_rotations_right < target_rotations_right:
        print("3", file=stderr)
        while current_rotations_left > target_rotations_left or current_rotations_right < target_rotations_right: # how its done in tank onForRotations
            current_rotations_left = largeMotor_Left.angle() 
            current_rotations_right = largeMotor_Right.angle()
            if stop():
                break
            if current_rotations_left <= target_rotations_left or current_rotations_right >= target_rotations_right:
                break
    # > > 
    # if left motor's current rotations is larger and the right current rotations are larger do the code
    elif current_rotations_left > target_rotations_left and current_rotations_right > target_rotations_right:
        print("4", file=stderr)
        while current_rotations_left > target_rotations_left or current_rotations_right > target_rotations_right: # how its done in tank onForRotations
            #re reading in the current rotations into the variable
            current_rotations_left = largeMotor_Left.angle() 
            current_rotations_right = largeMotor_Right.angle()
            #print("Right {}{}, Left {}{}".format(current_rotations_right, target_rotations_right, current_rotations_left, target_rotations_left),file = stderr)
            if stop():
                break
            if current_rotations_left <= target_rotations_left or current_rotations_right <= target_rotations_right:
                break
    robot.stop()


    print('Leaving Steering_rotations', file=stderr)

    #tells framework the function is completed 
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

#stopProcessing = False
#steering_rotations(lambda:stopProcessing, 0, -20, 2, 0)
