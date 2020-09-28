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

def blackline_to_line(stop, speed, sensor, lineSide, correction):
    rotations = rotations*360
    currentDegrees_left = largeMotor_Left.angle()
    currentDegrees_right = largeMotor_Right.angle()
    target_left = currentDegrees_left + rotations
    target_right = currentDegrees_right + rotations
    right_RLI = colourRight.reflection()
    left_RLI = colourLeft.reflection()
    target_RLI = 40
    
    #if the colour sensor that you are using = Right then do this part of the program (being called from defined section above)
    if sensor == "RIGHT":
        #Choosing which side of the line to follow
        
        if lineSide == "LEFT":
            while left_RLI > 20: 
                #and currentDegrees_right < target_right:
                currentDegrees_left = largeMotor_Left.angle()
                #currentDegrees_right = largeMotor_Right.angle()
                right_RLI = colourRight.reflection()
                left_RLI = colourLeft.reflection()
                error = right_RLI - target_RLI

                steering = 0

                if abs(error) < 5: #If the absaloute error (positive error) is smaller than 5
                    steering = error * 0.25

                elif abs(error) >= 5 and abs(error) <=10: #If the absaloute error (positive error) is larger of equal to 5 AND smaller than 10
                    steering = error * 0.5

                elif abs(error) >= 10 and abs(error) <=25: #If the absaloute error (positive error) is larger of equal to 10 AND smaller or equal to 25
                    steering = error * 1 

                elif abs(error) >= 25:
                    steering = error * 1.25
                
                #steering = error * correction

                robot.drive(speed=speed, turn_rate = steering)
                if stop():
                    break
        #Choosing which side of the line to follow
        elif lineSide == "RIGHT":
            while currentDegrees_left < target_left and currentDegrees_right < target_right:
                currentDegrees_left = largeMotor_Left.angle()
                currentDegrees_right = largeMotor_Right.angle()
                right_RLI = colourRight.reflection()
                error = target_RLI - right_RLI
                steering = error * correction
                robot.drive(speed=speed, turn_rate = steering)
                if stop():
                    break


    #if the colour sensor that you are using = Right then do this part of the program (being called from defined section above)                  

    elif sensor == "LEFT":

        #Choosing which side of the line to follow
        if lineSide == "RIGHT":
            
            while currentDegrees_left < target_left and currentDegrees_right < target_right:
                currentDegrees_left = largeMotor_Left.angle()
                currentDegrees_right = largeMotor_Right.angle()
                left_RLI = colourLeft.reflection()
                error = target_RLI - right_RLI 
                steering = error * correction
                robot.drive(speed=speed, turn_rate = steering)
                if stop():
                    break

        #Choosing which side of the line to follow
        elif lineSide == "LEFT":
            while currentDegrees_left < target_left and currentDegrees_right < target_right:
                currentDegrees_left = largeMotor_Left.angle()
                currentDegrees_right = largeMotor_Right.angle()
                left_RLI = colourLeft.reflection()
                error = left_RLI - target_RLI 
                steering = error * correction
                robot.drive(speed=speed, turn_rate = steering)
                if stop():
                    break
    robot.drive.off()
