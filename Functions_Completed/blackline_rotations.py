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
def  blackline_rotations(stop, speed, rotations, sensor, lineSide, correction):
    print("In BlackLine_rotations", file=stderr)
    # calculate how far to drive in degrees
    rotations = rotations*360
    # saves the current positions of the motors
    currentDegrees_left = largeMotor_Left.angle()
    currentDegrees_right = largeMotor_Right.angle()
    # calculates the target rotations for each motor
    target_left = currentDegrees_left + rotations
    target_right = currentDegrees_right + rotations
    # saves the current RLI for each sensor 
    right_RLI = colourRight.reflection()
    left_RLI = colourLeft.reflection()
    # RLI it should be reading if following the line
    target_RLI = 40

    if sensor == "RIGHT": # if using the right sensor 
        if lineSide == "LEFT": # if on left side of the line
            while currentDegrees_left < target_left: 
                # saves current motor position and RLI
                currentDegrees_left = largeMotor_Left.angle()
                right_RLI = colourRight.reflection()
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
            while currentDegrees_left < target_left and currentDegrees_right < target_right:
                # saves the current motor posoitions and RLI 
                currentDegrees_left = largeMotor_Left.angle()
                currentDegrees_right = largeMotor_Right.angle()
                right_RLI = colourRight.reflection()
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
            while currentDegrees_left < target_left and currentDegrees_right < target_right:
                # saves the motor positions and the current RLI
                currentDegrees_left = largeMotor_Left.angle()
                currentDegrees_right = largeMotor_Right.angle()
                left_RLI = colourLeft.reflection()
                # calculates the error 
                error = target_RLI - right_RLI 
                steering = 0
                steering = error * 0.5
               
                robot.drive(speed=speed, turn_rate = steering)
                
                # if stop is true then exit the function
                if stop():
                    break
        # if following the left side of the lien
        elif lineSide == "LEFT":
            while currentDegrees_left < target_left and currentDegrees_right < target_right:
                # saves the motor position and RLI
                currentDegrees_left = largeMotor_Left.angle()
                currentDegrees_right = largeMotor_Right.angle()
                left_RLI = colourLeft.reflection()
                # calculates the error
                error = left_RLI - target_RLI 
                steering = 0
                steering = error * 0.5
     
                robot.drive(speed=speed, turn_rate = steering)
                
                # if stop is true then exit the function
                if stop():
                     break
    robot.drive.off()
    print("Leaving BlackLine_rotations", file=stderr)
stopProcessing=False
#blackline_rotations(lambda:stopProcessing, 10, 10, 'RIGHT', 'RIGHT', 50)

