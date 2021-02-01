
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

def reset_gyro_2(stop, threadKey):
    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    # loop until the gyro is reset properly 
    while True:
        calibrationSuccess = False
        try:
            gyro = ColorSensor(Port.S4)
        except:
            print("failed to switch port to port 2")
        finally:
            gyro = GyroSensor(Port.S4)
            colourRight = ColorSensor(Port.S2)
            time.sleep(1)

        

        retries = 12 

        while retries > 0:  
           prev_gyro_reading = gyro.angle()   # Initial reading.  We will compare it over time to see if it is changing
           print(prev_gyro_reading, file = stderr)       
           time.sleep(0.3)   
           retries = retries - 1
           current_gyro_reading = gyro.angle()
           print(current_gyro_reading, file = stderr)
           # check if the gyro has reset properly
           if round(prev_gyro_reading, 1) == round(current_gyro_reading, 1): 
               print('gyro has stabilised')
               calibrationSuccess = True
               break

        if calibrationSuccess:
            gyro.reset_angle(0) 
            break

    # log leaving the function
    ev3.speaker.play_file(SoundFile.READY)
    print('Leaving recalibrate_gyro', file=stderr)

    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)



'''#!/usr/bin/env pybricks-micropython
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

def reset_gyro_2(stop, threadKey):
    # log the function starting 
    print("In recalibrate_gyro", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    while True:
        prev_gyro_reading = gyro.angle()
        time.sleep(0.3)
        current_gyro_reading = gyro.angle()
        
        if current_gyro_reading == prev_gyro_reading:
            gyro.reset_angle(0)
            break


    print("finished reset gyro 2")
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
    '''