#!/usr/bin/env pybricks-micropython
# - Micropython -
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor, GyroSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
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

# turn a single motor for a set amount of time 
def motor_onForSeconds(stop, threadKey, motor, speed, seconds):
    # log the function starting
    print("In motor_onForSeconds", file=stderr)
    
    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    # if we needed an extra motor, defining it here prevents it from messing up other bits of code and allows us to unplug it after a run
    if motor == "extension":
        motor =  Motor(Port.A)

    # read the current time
    start_time = time.time()
    # turn the motor on 
    motor.run(speed=speed)
    # wait until the set amount of time has passed
    while time.time() < start_time + seconds: 
        # check if 'stopProcessing' flag is raised
        if stop():
            break
    
    # turn the motor off
    motor.stop()

    # log leaving the function 
    print('Leaving Motor_onForSeconds', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

#stopProcessing=False
#Motor_onForSeconds(lambda:stopProcessing, 0, motor = panel, speed = 200, seconds = 3)