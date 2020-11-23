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
def reset_gyro(stop, threadKey):
    # log the function starting 
    print("In recalibrate_gyro", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    repeat = True
    x = gyro.angle()
    time.sleep(0.25)
    y = gyro.angle()
    if x == y:
        gyro.reset_angle(0)
        repeat = False


    # loop until the gyro is reset properly 
    while repeat:
        calibrationSuccess = False
        gyro.speed()
        gyro.angle()
        retries = 12 #After resetting the gyro, we will see if it has stabilised 12 times.  If not, we will reset the gyro again. 
        prev_gyro_reading = gyro.angle()  # Initial reading.  We will compare it over time to see if it is changing
        print(prev_gyro_reading, file = stderr)

        while retries > 0:         
           time.sleep(0.3)      # not sure how long this should be: Worst case its 12 x 0.3 seconds or 3.6 seconds before it does the whole thing again
           retries = retries - 1
           current_gyro_reading = gyro.angle()
           print(current_gyro_reading, file = stderr)
           # check if the gyro has reset properly
           # << I am not sure if we should use `int()` (which converts to an integer) or `round()` (which can round to a specified number of decimal places).  
           # If you use `int()` it may not be accurate enough and cause the gyro to appear stable even if it is not.  
           # What values does `gyro.angle()` return?  If there are many decimal places then rounding to one or two decimal places might make better sense.
           if round(prev_gyro_reading, 1) == round(current_gyro_reading, 1): 
               print('gyro has stabilised')
               calibrationSuccess = True
               break
        # Did the gyro reset correctly?
        if calibrationSuccess:
            # Now that the sensor has calibrated to a stable vale, reset it so that the current direction is considered 0.
            gyro.reset_angle(0) 
            break

    # log leaving the function
    ev3.speaker.play_file(SoundFile.READY)
    print('Leaving recalibrate_gyro', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

#stopProcessing=False
#reset_gyro(lambda:stopProcessing, 0)

"""#!/usr/bin/env pybricks-micropython
# - Micropython -
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor, GyroSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
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
def reset_gyro(stop,threadKey):
    # log the function starting 
    print("In reset_gyro", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])
    
    # recalibrates the gyro angle by switching between modes 
    time.sleep(0.3)
    gyro.speed()
    gyro.reset_angle(0)
    time.sleep(0.3)

    # print the current gyro reading to check for gyro creep
    while True:
        current_gyro_reading = gyro.angle()
        print(current_gyro_reading, file = stderr)
        time.sleep(0.3)
        gyro.speed()
        gyro.reset_angle(0)
        time.sleep(0.3)
        if int(current_gyro_reading) == 0:
            break
        if stop():
            break   

    # log leaving the function
    print('Leaving reset_gyro', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

#stopProcessing=False
#reset_gyro(lambda:stopProcessing, 0)"""