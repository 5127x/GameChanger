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

def gyro_target(stop, speed, rotations, target):
    print("In StraightGyro_target", file=stderr)
    current_degrees = largeMotor_Left.angle() 
    rotations = rotations * 360
    target_rotations= current_degrees + rotations
    current_gyro_reading = gyro.angle
    # print("Current Gyro Reading: {}".format(current_gyro_reading))
    while float(current_degrees) < target_rotations:
        if stop(): 
            break

        # reading in current gyro and  rotations
        current_gyro_reading=gyro.angle
        current_degrees = largeMotor_Left.angle()

        #if the gyro is smaller than the target
        if current_gyro_reading < target:
            correction = target - current_gyro_reading # calculate full error by target - gyro
            correction = correction * .25 # 1/4 of the correction (so the robot doesn't over correct)
            robot.drive(turn_rate = -correction , speed = speed) # turn by the correctuion and doesn't over correct

        #if the gyro is larger than the target
        if current_gyro_reading > target:
            correction = target - current_gyro_reading # calculate full error by target - gyro
            correction = correction * .25  # 1/4 of the correction (so the robot doesn't over correct)
            robot.drive(turn_rate = -correction , speed = speed) # turn by the correctuion and doesn't over correct

        #if the gyro is == to the target just go straight
        if current_gyro_reading == target:
            robot.drive(turn_rate = 0 , speed = speed)

        # if the current rotations is larger than the target then break the loop which will stop the robot
        if float(current_degrees) >= target_rotations:
            break

        if stop():
            break

    tank_block.off()
    print('Leaving StraightGyro_target', file=stderr)

#stopProcessing=False
#StraightGyro_target(lambda:stopProcessing, speed=30, rotations=3)