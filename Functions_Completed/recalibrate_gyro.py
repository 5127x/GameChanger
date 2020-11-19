#!/usr/bin/env pybricks-micropython
# - Micropython -
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor, GyroSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile
# basic import s
import os
import time
from sys import stderr
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# define motors, sensor and the brick
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

# recalibrates the gyro before a run
def recalibrate_gyro(stop, threadKey):
    # log the function starting 
    print("In recalibrate_gyro", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    # loop until the gyro is reset properly 
    while True: 
        time.sleep(0.5)
        gyro.speed()
        gyro.angle()
        gyro.reset_angle(0)
        time.sleep(1.7)
        
        current_gyro_reading = gyro.angle()
        print(current_gyro_reading, file = stderr)

        time.sleep(0.3) #new bit
        x = gyro.angle() #new bit

        # check if the gyro has reset properly
        if int(current_gyro_reading) == 0 and x == 0: #new bit
            print('gyro reads 0')
            break
        
        # check if 'stopProcessing' flag has been raised 
        if stop():
            break

    # log leaving the function
    ev3.speaker.play_file(SoundFile.READY)
    print('Leaving recalibrate_gyro', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

#stopProcessing=False
#reset_gyro(lambda:stopProcessing, 0)