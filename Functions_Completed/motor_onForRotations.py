#!/usr/bin/env pybricks-micropython
# - Micropython -
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor, GyroSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from sys import stderr
import time
import os


ev3 = EV3Brick()
#robot = DriveBase(largeMotor_Left, largeMotor_Right, wheel_diameter=62, axle_track=104)
#_________________________________________________________________________________________________________________________________

def motor_onForRotations(stop, threadKey, motor, speed, rotations, gearRatio): 
    print("In Motor onForRotations", file=stderr)
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    if motor == "extension":
        motor =  Motor(Port.A)

    # read the motor position (degrees since there isn't a way to read rotations)
    current_degrees = motor.angle() 
    
    # take the gearRatio into account
    rotations = rotations*gearRatio

    # create target rotations
    target_rotations = rotations * 360
    if speed > 0:
        target_rotations = current_degrees + target_rotations
    elif speed < 0:
        target_rotations = current_degrees - target_rotations
    # turn the motor on until current_degrees matches target_rotations
    motor.run(speed=speed)
    
    # Just a note. The larger and smaller is because if the robot is going backward. 
    
    if current_degrees > target_rotations:# current degrees can also be how many rotations a motor has done
        while current_degrees > target_rotations: # while current rotations is larger than target
            current_degrees = motor.angle() # reading current rotations into the paramater
            # continue speed until one of the following staements become true
            if stop():
                break
            if current_degrees <= target_rotations:
                break

    elif current_degrees < target_rotations:
        while current_degrees < target_rotations: # while current rotations is smaller than target
            current_degrees = motor.angle() # reading current rotations into the paramater
            # continue speed until one of the following staements become true
            if stop():
                break
            if current_degrees >= target_rotations:
                break
    motor.stop()
    print('Leaving onForRotations', file=stderr)
    
    #tells framework the function is completed 
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

#panel = Motor(Port.D)
#stopProcessing=False
#motor_onForRotations(lambda:stopProcessing, threadKey=0, motor=panel, speed=-30, rotations=2, gearRatio=1)