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

def blackline_to_line(stop, threadKey, speed, sensor, lineSide, correction):

    print("In blackline_to_line", file= stderr)
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    # RLI it should be reading if following the line
    target_RLI = 40

    # saves the current RLI for each sensor 
    right_RLI = colourRight.reflection()
    left_RLI = colourLeft.reflection()

    if sensor == "RIGHT": # if using the right sensor 
        if lineSide == "LEFT": # if on left side of the line
            while True:
                # Reading RLI
                right_RLI = colourRight.reflection()
                left_RLI = colourLeft.reflection()
                
                #testing if your robot can see the black line with the left sensor
                #if left_RLI >= 85:
                    #print("White line detected", file = stderr)
                if left_RLI <= 10:
                    print("Black line deteted. BREAK", file = stderr)
                    break

                # calulate the error
                error = right_RLI - target_RLI
                steering = 0
                steering = error * 0.5
                robot.drive(speed=speed, turn_rate = steering)
                
                # if stop is True then exit the function
                if stop():
                    break

                sleep(0.01)

        # if on the right side of the lien
        elif lineSide == "RIGHT":
            while True:
                # Reading RLI
                right_RLI = colourRight.reflection()
                left_RLI = colourLeft.reflection()
                
                #testing if your robot can see the black line with the left sensor
                #if left_RLI >= 85:
                #   print("White line detected", file = stderr)
                if left_RLI <= 10:
                    print("Black line deteted. BREAK", file = stderr)
                    break


                # calculates the error
                error = target_RLI - right_RLI
                steering = 0
                steering = error * 0.5
                robot.drive(speed=speed, turn_rate = steering)
                
                # if stop is true then exit the function
                if stop():
                    break
    
    # if the left sensor 
    elif sensor == "LEFT":
        # if following the right side of the lien
        if lineSide == "RIGHT":
            while True:
                # Reading RLI
                right_RLI = colourRight.reflection()
                left_RLI = colourLeft.reflection()

                #testing if your robot can see the black line with the left sensor
               # if right_RLI >= 85:
                    #print("White line detected", file = stderr)
                if right_RLI <= 15:
                    print("Black line deteted. BREAK", file = stderr)
                    break


                # calculates the error 
                error = target_RLI - right_RLI 
                steering = 0
                steering = error * 0.5
               
                robot.drive(speed=speed, turn_rate = steering)
                
                # if stop is true then exit the function
                if stop():
                    break

        # if following the left side of the line
        elif lineSide == "LEFT":
            while True:
                # Reading RLI
                right_RLI = colourRight.reflection()
                left_RLI = colourLeft.reflection()

                #testing if your robot can see the black line with the left sensor
                #if right_RLI >= 85:
                    #print("White line detected", file = stderr)
                if right_RLI <= 15:
                    print("Black line deteted. BREAK", file = stderr)
                    break


                # calculates the error
                error = left_RLI - target_RLI 
                steering = 0
                steering = error * 0.5
     
                robot.drive(speed=speed, turn_rate = steering)
                
                # if stop is true then exit the function
                if stop():
                     break
    robot.stop()
    #tells framework the function is completed 
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)