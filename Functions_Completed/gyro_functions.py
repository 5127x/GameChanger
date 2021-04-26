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

# define the motors, sensors and the brick
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

""" 

Still a little more tweaking to be done 

"""

# calibrate the gyro 
def gyro_calibrate(threadKey):
    print("In gyro_calibrate", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    time.sleep(0.5)
    gyro.speed()
    gyro.angle()
    time.sleep(3)

    # log leaving the function
    print('Leaving gyro_calibrate', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# use the gyro to drive in a straight line facing the given direction for a set number of rotations
def gyro_target(stop, threadKey, speed, rotations, target, correction):
    # log the function starting
    print("In gyro_target", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    # read the env var into a normal va
    gyro_reading_env_var = float(os.environ['gyro_reading_env_var'])
    # read the current degrees heading and the current motor positions 
    current_gyro_reading = gyro.angle() - gyro_reading_env_var
    current_rotations = largeMotor_Left.angle() 
    # create 'target_rotations' for how far the robot should drive in degrees 
    rotations = rotations * 360
    target_rotations= current_rotations + rotations
    

    # loop until the robor has driven far enough
    while float(current_rotations) < target_rotations:
    
        # reading in current degrees heading and current motor positions 
        current_gyro_reading=gyro.angle() - gyro_reading_env_var
        current_rotations = largeMotor_Left.angle()

        # if facing to the left of the target
        if current_gyro_reading < target:
            # calculate the error
            error = target - current_gyro_reading 
            # calculate the needed steering to compensate 
            steering = error * correction 

            # the robot drives forward 
            robot.drive(turn_rate = steering , speed = speed) 

        # if facing to the right of the target
        if current_gyro_reading > target:
            # calculate the error 
            error = target - current_gyro_reading 
            # calculate the needed steering to compensate 
            steering = error * correction  

            # the robot drives forward 
            robot.drive(turn_rate = steering , speed = speed)

        # if perfectly straight
        if current_gyro_reading == target:
            # the robot drives forward 
            robot.drive(turn_rate = 0 , speed = speed)

        # check if the robot has driven far enough
        if current_rotations >= target_rotations:
            break
        
        # check if the 'stopProcessing' flag is raised 
        if stop():
            break

    # stop the robot
    robot.stop()

    # log leaving the function
    print('Leaving gyro_target', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# use the gyro to drive in a straight line facing the given direction until the sensor sees a line
def gyro_target_to_line(stop, threadKey, speed, sensor, target, correction):
    # log the function starting
    print("In gyro_target_to_line", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    gyro_reading_env_var = float(os.environ['gyro_reading_env_var'])
    # read the current degrees heading and the current RLI values
    current_gyro_reading = gyro.angle() - gyro_reading_env_var
    if sensor == "RIGHT":
        RLI = colourRight.reflection()
    elif sensor == "LEFT":
        RLI = colourLeft.reflection()

    # loop
    while True:
        # read the current degrees heading and the current RLI values
        current_gyro_reading=gyro.angle() - gyro_reading_env_var
        if sensor == "RIGHT":
            RLI = colourRight.reflection()
        elif sensor == "LEFT":
            RLI = colourLeft.reflection()

        # if facing to the left of the target
        if current_gyro_reading < target:
            # calculate the error
            error = target - current_gyro_reading 
            # calculate the needed steering to compensate 
            steering = error * correction 

            # the robot drives forward
            robot.drive(turn_rate = steering , speed = speed) 

        # if facing to the right of the target
        if current_gyro_reading > target:
            # calculate the error
            error = target - current_gyro_reading 
            # calculate the needed steering to compensate 
            steering = error * correction  

            # the robot drives forward
            robot.drive(turn_rate = steering , speed = speed)

        # if perfectly straight
        if current_gyro_reading == target:
            # the robot drives forward
            robot.drive(turn_rate = 0 , speed = speed)

        # check if there is a black line
        if RLI <= 15:
            break

        # check if the 'stopProcessing' flag has been raised
        if stop():
            break

    # stop the robot 
    robot.stop()

    # log leaving the function 
    print('Leaving gyro_target_to_line', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# use the gyro to drive in a straight line facing the direction it currently faces for a set number of rotations
def gyro_current(stop, threadKey, speed, rotations, correction):
    # log the function starting 
    print("In gyro_current", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    gyro_reading_env_var = float(os.environ['gyro_reading_env_var'])

    # read the current motor positions
    current_rotations = largeMotor_Left.angle() 

    # create 'target_rotations' for how far the robot should drive in degrees 
    rotations = rotations * 360
    target_rotations= current_rotations + rotations

    # create the target degrees
    target = gyro.angle() - gyro_reading_env_var
    # read the current degrees heading  
    current_gyro_reading = target

    # loop until the robot has driven far enough
    while float(current_rotations) < target_rotations: 
        # read the current motor position and the current degrees heading 
        current_gyro_reading=gyro.angle() - gyro_reading_env_var
        current_rotations = largeMotor_Left.angle() - gyro_reading_env_var

        # if facing to the right of the target
        if current_gyro_reading > target:
            # calculate the error 
            error = target - current_gyro_reading 
            # calculate the needed steering to compensate
            steering = error * correction 

            # the robot drives forward 
            robot.drive(turn_rate = steering , speed = speed) 

        # if facing to the left of the target
        if current_gyro_reading < target:
            # calculate the error 
            error = target - current_gyro_reading
            # calculated the needed steering to compensate 
            steering = error * correction 

            # the robot drives forward 
            robot.drive(turn_rate = steering , speed = speed) 

        # if perfectly straight 
        if current_gyro_reading == target:
            # the robot drives forward
            robot.drive(turn_rate = 0 , speed = speed)

        # check if the robot has driven far enough 
        if float(current_rotations) >= target_rotations:
            break

        # check if the 'stopProcessing' flag has been raised
        if stop():
            break

    # stop the robot 
    robot.stop()

    # log leaving the function
    print('Leaving gyro_current', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# use the gyro to drive in a straight line facing the direction it currently faces until the sensor sees a line
def gyro_current_to_line(stop, threadKey, speed, sensor, correction):
    # log the function starting 
    print("In gyro_current_to_line", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    gyro_reading_env_var = float(os.environ['gyro_reading_env_var'])

    # create the target degrees
    target = gyro.angle() - gyro_reading_env_var
    # read the current degrees heading and the current RLI values
    current_gyro_reading = target
    if sensor == "RIGHT":
        RLI = colourRight.reflection()
    elif sensor == "LEFT":
        RLI = colourLeft.reflection()

    # loop 
    while True:  
        # read the current degrees heading and the current RLI values
        current_gyro_reading=gyro.angle() - gyro_reading_env_var
        if sensor == "RIGHT":
            RLI = colourRight.reflection()
        elif sensor == "LEFT":
            RLI = colourLeft.reflection()
        
        # if facing to the right of the target
        if current_gyro_reading > target:
            # calculate the error 
            error = target - current_gyro_reading 
            # calculate the needed steering to compensate
            steering = error * correction 

            # the robot drives forward 
            robot.drive(turn_rate = steering , speed = speed) 

        # if facing to the left of the target
        if current_gyro_reading < target:
            # calculate the error 
            error = target - current_gyro_reading
            # calculated the needed steering to compensate 
            steering = error * correction 

            # the robot drives forward 
            robot.drive(turn_rate = steering , speed = speed) 

        # if perfectly straight 
        if current_gyro_reading == target:
            # the robot drives forward
            robot.drive(turn_rate = 0 , speed = speed)

        # check if there is a black line
        if RLI <= 15:
            break

        # check if the 'stopProcessing' flag has been raised 
        if stop():
            break

    # stop the robot 
    robot.stop()

    # log leaving the function
    print('Leaving gyro_current_to_line', file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def gyro_turning(stop, threadKey, speed, degrees): 
    # create the target degrees
    print("In Turn_degrees", file=stderr)

    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])
    
    gyro_reading_env_var = float(os.environ['gyro_reading_env_var'])

    #read in the current gyro
    current_gyro_reading = gyro.angle() - gyro_reading_env_var
    target_degrees = current_gyro_reading + degrees

    #_____________If turning Left__________________________________
    while target_degrees > current_gyro_reading: 
        print(speed, file = stderr)

        #same concept as a tank block however bc we dont have access had to turn on both motors
        largeMotor_Right.run(speed=-speed)
        largeMotor_Left.run(speed=speed) 
        
        #print(current_gyro_reading,file=stderr)

        if target_degrees > current_gyro_reading:
            current_gyro_reading = gyro.angle() - gyro_reading_env_var
            if current_gyro_reading == target_degrees:
                break
            if stop():
                break

    #_____________If turning Right__________________________________
    while target_degrees < current_gyro_reading:
        largeMotor_Right.run(speed=speed)
        largeMotor_Left.run(speed=-speed)
        
        #print(current_gyro_reading,file=stderr)

        if target_degrees <current_gyro_reading:
            current_gyro_reading = gyro.angle()
            if current_gyro_reading == target_degrees:
                break
            if stop():
                break

    robot.stop()
    print('Leaving Turn_degrees', file= stderr)

    #tells framework the function is completed 
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# 
def gyro_turn_to_target(stop, threadKey, speed, degrees):
    
    # log the function starting 
    #print(degrees, file=stderr)
    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    gyro_reading_env_var = float(os.environ['gyro_reading_env_var'])

    # read the current degrees heading 
    current_gyro_reading = gyro.angle()
    #print("current val", current_gyro_reading, file=stderr)
    
    # if facing to the left of the target
    if current_gyro_reading < degrees:
        # start turning the robot 
        largeMotor_Left.run(speed=speed)
        largeMotor_Right.run(speed=-speed)

        # loop until facing the correct angle 
        while current_gyro_reading < degrees:
            print("current gyro val", gyro.angle(), file=stderr)
            #print(current_gyro_reading, file=stderr)
            # read the current degress heading 
            current_gyro_reading = gyro.angle() - gyro_reading_env_var

            # check if the robot has turned far enough
            if current_gyro_reading >= degrees:
                largeMotor_Left.run(speed=-speed/2)
                largeMotor_Right.run(speed=speed/2)

            if current_gyro_reading == degrees:
                break

            # check if the 'stopProcessing' flag has been raised 
            if stop():
                break

    # if facing to the right of the target 
    elif current_gyro_reading > degrees:
        # start turning the robot 
        largeMotor_Left.run(speed=-speed)
        largeMotor_Right.run(speed=speed)

        # loop until the robot has turned far enough 
        while current_gyro_reading > degrees:
            print("current gyro val", gyro.angle(), file=stderr)
            #print(current_gyro_reading, file=stderr)
            # read the current degrees heading                
            current_gyro_reading = gyro.angle() - gyro_reading_env_var

            # check if the robot had turned far enough 
            if current_gyro_reading <= degrees:
                largeMotor_Left.run(speed=speed/2)
                largeMotor_Right.run(speed=-speed/2)
            if current_gyro_reading == degrees:
                break

            # check if the 'stopProcessing' flag has been raised 
            if stop():
                break

    # stop the robot 
    robot.stop()

    # log leaving the function
    print("Leaving gyro_turn_to_target", file=stderr)   
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)   
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#stopProcessing=False
#gyro_calibrate(0)
#gyro_target(lambda:stopProcessing, 0, speed = 30, rotations = 3, target = 0, correction = 0.8)
#gyro_target_to_line(lambda:stopProcessing, 0, speed = 30, sensor = 'RIGHT', target = 0, correction = 0.8)
#gyro_current(lambda:stopProcessing, 0, speed = 150, rotations = 2, correction = 0.5)
#gyro_current_to_line(lambda:stopProcessing, 0, speed = 150, sensor = 'RIGHT', correction = 0.5)
#gyro_turning(lambda:stopProcessing, speed=30, degrees=90)
#gyro_turn_to_target(lambda:stopProcessing, 0, speed=30, degrees=90)