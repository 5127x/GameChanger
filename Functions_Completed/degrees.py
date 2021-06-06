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

def panel_motor_degrees_reset(stop, threadKey):
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    panel.reset_angle(0)
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def turn_current_degrees(stop, threadKey, speed, target_degrees):
    print("In turn_current_degrees", file=stderr)
    print(target_degrees)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    #__________________
    current_degrees = panel.angle()
    
    if float(target_degrees) > 0:
        #print("speed is positive", file = stderr)
        panel.run(speed = speed)
        while float(speed) > 0:
            print(current_degrees, file = stderr)
            current_degrees = panel.angle()

            if float(current_degrees) >= float(target_degrees):
                print("met requirments")
                panel.brake()
                break 


            if stop():
                print("stop")
                panel.brake()            
                break

        while float(speed) <  0:
            #print("speed is negative", file=stderr)
            print(current_degrees, file = stderr)
            current_degrees = panel.angle()
            if float(current_degrees) <= float(target_degrees):
                panel.brake()
                break 

            if stop():
                panel.brake()
                break
    
    if float(target_degrees) < 0:
        panel.run(speed = -speed)
        while float(speed) > 0:
            print("speed is positive", file = stderr)
            print(current_degrees, file = stderr)
            current_degrees = panel.angle()

            if float(current_degrees) <= float(target_degrees):
                print("met requirments")
                panel.brake()
                break 


            if stop():
                print("stop")
                panel.brake()            
                break

        while float(speed) <  0:
            print("speed is negative", file=stderr)
            print(current_degrees, file = stderr)
            current_degrees = panel.angle()
            if float(current_degrees) >= float(target_degrees):
                panel.brake()
                break 

            if stop():
                panel.brake()
                break
        # if facing to the left of the

    # stop the robot
    robot.stop()
    print('Leaving turn_target', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
