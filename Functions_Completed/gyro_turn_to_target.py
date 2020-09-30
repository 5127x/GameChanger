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

#_________________________________________________________________________________________________________________________________

def gyro_turn_to_target(stop, threadKey, speed, degrees):
    print("In gyro_turn_to_target", file=stderr)
    current_gyro_reading = gyro.angle()

    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    # if the gyro is smaller than degrees (parameter from above)
    if current_gyro_reading < degrees:
        largeMotor_Left.run(speed=speed)
        largeMotor_Right.run(speed=-speed)

        while current_gyro_reading < degrees:
            #print("Current Gyro: {}".format (float(current_gyro_reading)), file=stderr)    
            # read in the gyro value            
            current_gyro_reading = gyro.angle()
            #gyro reading is larger than target (once reached the degrees) stop program
            if current_gyro_reading >= degrees:
                break
            if stop():
                break

    # if the gyro is larger than degrees (parameter from above)
    elif current_gyro_reading > degrees:
        largeMotor_Left.run(speed=-speed)
        largeMotor_Right.run(speed=speed)

        while current_gyro_reading > degrees:
            #print("Current Gyro: {}".format (float(current_gyro_reading)), file=stderr)                
            current_gyro_reading = gyro.angle()
            #gyro reading is smaller than target (once reached the degrees) stop program
            if current_gyro_reading <= degrees:
                break
            if stop():
                break

    robot.stop()
    print("Leaving Turn_from_start_position", file=stderr)   

    #tells framework the function is completed 
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)   

    #print("Current Gyro: {}".format (float(current_gyro_reading)), file=stderr)
