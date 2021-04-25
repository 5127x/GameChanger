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

#define the motors, sensors and the brick
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

# turn a single motor for a set number of rotations 
def motor_onForRotations(stop, threadKey, motor, speed, rotations, gearRatio): 
    # log the function starting 
    print("In motor_onForRotations", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    # if we needed an extra motor, defining it here prevents it from messing up other bits of code and allows us to unplug it after a run
    if motor == "extension":
        motor =  Motor(Port.A)

    # read the motor position 
    current_degrees = motor.angle() 
    # adjust the rotations goal for the gearing ratio of the motor/attachment 
    rotations = rotations*gearRatio
    
    # create 'target_rotations' for how far the motor should turn in degrees
    target_rotations = rotations * 360
    if speed > 0:
        target_rotations = current_degrees + target_rotations
    elif speed < 0:
        target_rotations = current_degrees - target_rotations
    
    # turn the motor on until current_degrees matches target_rotations
    motor.run(speed=speed)
    
    # if the motor is turning backwards 
    if current_degrees > target_rotations: 
        # loop until the motor has turned enough
        while current_degrees > target_rotations: 
            current_degrees = motor.angle() 
            # check if 'stopProcessing' flag is raised
            if stop():
                break
            # check if the motor has turned enough
            if current_degrees <= target_rotations:
                break
    
    # if the motor is turning forwards
    elif current_degrees < target_rotations:
        # loop until the motor has turned enough
        while current_degrees < target_rotations: 
            current_degrees = motor.angle() 
            # check if 'stopProcessing' flag is raised
            if stop():
                break
            # check if the motor has turned enough
            if current_degrees >= target_rotations:
                break
    
    # turn the motor off
    motor.stop()

    # log leaving the function
    print('Leaving onForRotations', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# turn a single motor for a set amount of time 
def motor_onForSeconds(stop, threadKey, motor, speed, seconds):
    # log the function starting
    print("In motor_onForSeconds", file=stderr)
    
    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    # read the current time
    start_time = time.time()
    # turn the motor on 
    motor.run(speed=speed)
    # wait until the set amount of time has passed
    while time.time() < start_time + seconds: 
        # check if 'stopProcessing' flag is raised
        print("Not met time limit", file=stderr)
        if stop():
            break
    
    # turn the motor off
    print("stopping motor", file=stderr)
    motor.stop()


    # log leaving the function 
    print('Leaving Motor_onForSeconds', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#stopProcessing=False
#motor_onForRotations(lambda:stopProcessing, 0, motor = panel, speed = 200, rotations = 2, gearRatio = 1)
#Motor_onForSeconds(lambda:stopProcessing, 0, motor = panel, speed = 200, seconds = 3)