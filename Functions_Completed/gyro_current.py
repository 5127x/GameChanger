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
def gyro_current(stop, threadKey, speed, rotations, correction):
    print("In StraightGyro_current", file=stderr)

    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    current_rotations = largeMotor_Left.angle() 
    rotations = rotations * 360
    target_rotations= current_rotations + rotations
    target = gyro.angle()
    current_gyro_reading = target
    # print("Current Gyro Reading: {}".format(current_gyro_reading))

    while float(current_rotations) < target_rotations: # if the currentm rotations is smaller than the target rotations
        if stop(): 
            break
        #recording the gyro reading  and the current rotations
        current_gyro_reading=gyro.angle()
        current_rotations = largeMotor_Left.angle()

        # if the gyro reading is smaller than the target (Going to the right)
        if current_gyro_reading > target:
            error = target - current_gyro_reading #figure out correction by target gyro reading - the current reading
            steering = error * correction # find a 1/4 of the correction 
            robot.drive(turn_rate = steering , speed = speed) #turns by the corrrection

        # if the gyro reading is larger than the target (Going to the left)
        if current_gyro_reading < target:
            error = target - current_gyro_reading#figure out correction by target gyro reading - the current reading
            steering = error * correction # find a 1/4 of the correction 
            robot.drive(turn_rate = steering , speed = speed) #turns by the corrrection

        # if the current gyro = the target just continue straight
        if current_gyro_reading == target:
            robot.drive(turn_rate = 0 , speed = speed)

        #if the current rotations is larger than the target break which will stop the loop
        if float(current_rotations) >= target_rotations:
            break
        if stop():
            break
    robot.stop()
    print('Leaving StraightGyro_current', file=stderr)
    #tells framework the function is completed 
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

#stopProcessing=False
#gyro_current(lambda:stopProcessing,0, speed=90, rotations=20, correction=0.5)
