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

def StraightGyro_target_toLine(stop, speed, rotations, target, whiteOrBlack):

    print("In StraightGyro_target_toLine", file=stderr)
    current_degrees = largeMotor_Left.angle() 
    rotations = rotations * 360
    target_rotations= current_degrees + rotations
    current_gyro_reading = gyro.angle
    # print("Current Gyro Reading: {}"(current_gyro_reading))

    while float(current_degrees) < target_rotations:
        if stop(): 
            break
        current_gyro_reading = gyro.angle
        current_degrees = largeMotor_Left.angle()

        if current_gyro_reading < target: # If gyro reading is smaller than target reaading turn Right
            correction = target - current_gyro_reading # calculate the correction by the target - current
            correction = correction * .25 #turns by the corrrection
            robot.drive(turn_rate = -correction , speed = speed)


        if current_gyro_reading > target: # If gyro reading is larger than target reAading turn Left
            correction = target - current_gyro_reading # calculate the correction by the target - current
            correction = correction * .25 #turns by the corrrection
            robot.drive(turn_rate = -correction , speed = speed)

        # if the gyro is = to target just continue straight
        if current_gyro_reading == target:
            robot.drive(turn_rate = 0 , speed = speed)

        #if the current rotations is larger than target quit out of code
        if float(current_degrees) >= target_rotations:
            break

        if stop():
            break
    

    # Now find the line
    
    if not stop(): # if the key has not been taken out of the slot
        while True:
            if stop(): 
                break
            # reading in the colour values (RLI)
            currentRight_RLI = colourRight.reflected_light_intensity
            currentLeft_RLI = colourLeft.reflected_light_intensity

            # if the whiteOrBlack paramater is white then:
            if whiteOrBlack == "WHITE":
                if currentRight_RLI > 90 or currentLeft_RLI > 90: #if the left or right sensor read over 90 then stop the robot (done by breaking out of the loop)
                    break

            if whiteOrBlack == "BLACK":
                if currentRight_RLI < 10 or currentLeft_RLI < 10:#if the left or right sensor read under 10 then stop the robot (done by breaking out of the loop)
                    break
            
            #otherwise continue straight BUT go slower so the colours are easier to detect
            robot.drive(steering = 0 , speed = speed / 2)                


    tank_block.off()
    print('Leaving StraightGyro_target_toLine', file=stderr)

#stopProcessing=False
#StraightGyro_target_toLine(lambda:stopProcessing, speed=30, rotations=3, target=45, whiteOrBlack="WHITE")