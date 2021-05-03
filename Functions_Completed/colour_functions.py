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
#constant_target_RLI_ = 22

if 'Debugging' in os.environ:
    debugging = int(os.environ['Debugging'])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# follow a black line for a set number of rotations 
def blackline_rotations(stop, threadKey, speed, rotations, sensor, lineSide, correction):
    # setting up code
    # log the function starting 
    print("In blackline_rotations", file=stderr)
    
    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    if 'Debugging' in os.environ:
        debugging = int(os.environ['Debugging'])
    # adjust rotations to be in degrees
    rotations = rotations*360

    # read the current motor positions 
    currentDegrees_left = largeMotor_Left.angle()
    currentDegrees_right = largeMotor_Right.angle()

    # create a target of distance robot should drive
    target_left = currentDegrees_left + rotations
    target_right = currentDegrees_right + rotations
    
    # read the current RLI for each sensor 
    right_RLI = colourRight.reflection()
    left_RLI = colourLeft.reflection()
    
    # set the variables needed
    target_RLI = 40
    steering = 0

    #- - - - - - - - - - - - 
    #  using the right sensor 
    if sensor == "RIGHT": 
        # if following the left side of the line
        if lineSide == "LEFT": 
            # loop until the robot had driven far enough
            while currentDegrees_left < target_left: 
                # read the current motor positions and current RLI values
                currentDegrees_left = largeMotor_Left.angle()
                right_RLI = colourRight.reflection()
                if debugging == True:
                    print(right_RLI, file = stderr)
                    
                # calulate the error
                error = right_RLI - target_RLI
                # calculate the needed steering to compensate
                steering = error * correction

                # the robot drives forward
                robot.drive(speed=speed, turn_rate = steering)
                
                # check if the 'stop_processing' flag has been raised
                if stop():
                    break
                
                # wait a little before the next repetition
                time.sleep(0.001)
                
        # if following the right side of the line
        elif lineSide == "RIGHT":
            # loop until the robot had driven far enough
            while currentDegrees_left < target_left and currentDegrees_right < target_right:
                # read the current motor positions and the current RLI values 
                currentDegrees_left = largeMotor_Left.angle()
                currentDegrees_right = largeMotor_Right.angle()
                right_RLI = colourRight.reflection()

                #checking if need logging for debugging
                if debugging == True:
                    print(right_RLI, file = stderr)

                # calculate the error
                error = target_RLI - right_RLI
                # calculate the needed steering to compensate
                steering = error * correction

                # the robot drives forward
                robot.drive(speed=speed, turn_rate = steering)
                
                # check if the 'stopProcessing' flag has been raised
                if stop():
                    break

                # wait a little before the next repetition
                time.sleep(0.001)
    
    # if using the left sensor 
    elif sensor == "LEFT":
        # if following the right side of the line
        if lineSide == "RIGHT":
            # loop until the robot has driven far enough
            while currentDegrees_left < target_left and currentDegrees_right < target_right:
                # saves the current motor positions and the current RLI values 
                currentDegrees_left = largeMotor_Left.angle()
                currentDegrees_right = largeMotor_Right.angle()
                left_RLI = colourLeft.reflection()

                # checking if code needs debugging
                if debugging == True:
                    print(left_RLI, file = stderr)
                
                # calculate the error 
                error = target_RLI - left_RLI 
                # calculate the needed steering to compensate
                steering = error * correction
               
                # the robot drives forward
                robot.drive(speed=speed, turn_rate = steering)
                
                # check if the 'stopProcessing' flag has been raised
                if stop():
                    break

                # wait a little before the next repetition
                time.sleep(0.001)

        # if following the left side of the line
        elif lineSide == "LEFT":
            # loop until the robot has driven far enough
            while currentDegrees_left < target_left and currentDegrees_right < target_right:
                # saves the current motor positions and the current RLI values 
                currentDegrees_left = largeMotor_Left.angle()
                currentDegrees_right = largeMotor_Right.angle()
                left_RLI = colourLeft.reflection()

                #check if code needs debugging
                if debugging == True:
                    print(left_RLI, file = stderr)

                # calculate the error
                error = left_RLI - target_RLI 
                # calculate the steering needed to compensate 
                steering = error * correction

                # the robot drives forward
                robot.drive(speed=speed, turn_rate = steering)
                
                # check if the 'stopProcessing' flag has been raised 
                if stop():
                    break

                # wait a little before the next repetition
                time.sleep(0.001)

    # stop the robot 
    robot.stop()

    # log leaving the function
    print("Leaving blackLine_rotations", file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# follow a black line until the opposite sensor sees another line
def blackline_to_line(stop, threadKey, speed, sensor, lineSide, correction):
    # log the function starting 
    print("In blackline_to_line", file= stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    if 'Debugging' in os.environ:
        debugging = int(os.environ['Debugging'])
    # RLI it should be reading if following the line
    target_RLI = 40 #40

    # saves the current RLI for each sensor 
    right_RLI = colourRight.reflection()
    left_RLI = colourLeft.reflection()

    # if using the right sensor 
    if sensor == "RIGHT": 
        # if following the left side of the line
        if lineSide == "LEFT":
            # loop
            while True:
                # read the current RLI values
                right_RLI = colourRight.reflection()
                left_RLI = colourLeft.reflection()

                #check if code needs debuggig
                if debugging == True:
                    print("LeftRLI = {} RightRLI = {}".format(left_RLI, right_RLI), file = stderr)

                # check if there is a black line
                if left_RLI <= 15:
                    break

                # calulate the error
                error = right_RLI - target_RLI
                # calculate the needed steering to compensate
                steering = 0
                steering = error * correction

                # the robot drives forward 
                robot.drive(speed=speed, turn_rate = steering)
                
                # check if the 'stopProcessing' flag has been raised
                if stop():
                    break

                # wait a little before the next repetition
                time.sleep(0.001)

        # if following the right side of the line
        elif lineSide == "RIGHT":
            # loop
            while True:
                # read the current RLI values
                right_RLI = colourRight.reflection()
                left_RLI = colourLeft.reflection()

                #check if code needs debuggig
                if debugging == True:
                    print("LeftRLI = {} RightRLI = {}".format(left_RLI, right_RLI), file = stderr)
                
                # check if there is a black line
                if left_RLI <= 15:
                    break

                # calculate the error
                error = target_RLI - right_RLI
                # calculate the needed steering to compensate
                steering = 0
                steering = error * correction

                # the robot drives forward
                robot.drive(speed=speed, turn_rate = steering)
                
                # check if the 'stopProcessing' flag has been raised 
                if stop():
                    break

                # wait a little before the next repetition
                time.sleep(0.001)
    
    # if using the left sensor 
    elif sensor == "LEFT":
        # if following the right side of the line
        if lineSide == "RIGHT":
            # loop
            while True:
                # read the current RLI values
                right_RLI = colourRight.reflection()
                left_RLI = colourLeft.reflection()

                #check if code needs debuggig
                if debugging == True:
                    print("LeftRLI = {} RightRLI = {}".format(left_RLI, right_RLI), file = stderr)

                # check if there is a black line 
                if right_RLI <= 15:
                    break

                # calculate the error 
                error = target_RLI - right_RLI 
                # calculate the needed steering to compensate
                steering = 0
                steering = error * correction
               
                # the robot drives forward
                robot.drive(speed=speed, turn_rate = steering)
                
                # check if the 'stopProcessing' flag has been raised 
                if stop():
                    break

                # wait a little before the next repetition
                time.sleep(0.001)

        # if following the left side of the line
        elif lineSide == "LEFT":
            # loop
            while True:
                # read the current RLI values
                right_RLI = colourRight.reflection()
                left_RLI = colourLeft.reflection()

                #check if code needs debuggig
                if debugging == True:
                    print("LeftRLI = {} RightRLI = {}".format(left_RLI, right_RLI), file = stderr)

                # check if there is a black line 
                if right_RLI <= 15:
                    break

                # calculate the error
                error = left_RLI - target_RLI 
                # calculate the needed steering to compensate
                steering = 0
                steering = error * correction
     
                # the robot drives forward 
                robot.drive(speed=speed, turn_rate = steering)
                
                # check if the 'stopProcessing' flag has been raised
                if stop():
                    break

                # wait a little before the next repetition
                time.sleep(0.001)

    # stop the robot 
    robot.stop()

    # log leaving the function
    print("Leaving blackline_to_line", file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# follow a black line until the opposite sensor sees another line
def run_to_blackline(stop, threadKey, speed, sensor):
    # log the function starting 
    print("In run to blackline", file= stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])
    
    if 'Debugging' in os.environ:
        debugging = int(os.environ['Debugging'])

    # RLI it should be reading if following the line
    target_RLI = 40 #40

    # saves the current RLI for each sensor 
    right_RLI = colourRight.reflection()
    left_RLI = colourLeft.reflection()

    robot.drive(turn_rate = 0, speed= speed)

    while True:
        right_RLI = colourRight.reflection()
        left_RLI = colourLeft.reflection()
        # if using the right sensor 
        if sensor == "RIGHT": 
            if debugging == True:
                print("RightRLI = {}".format(right_RLI), file = stderr)
            if right_RLI < target_RLI:
                break

        # if using the left sensor 
        elif sensor == "LEFT":
            if left_RLI < target_RLI:
                print("left_RLI = {}".format(left_RLI), file = stderr)
                print(left_RLI)
                break
        if stop():
            break

        # wait a little before the next repetition
        time.sleep(0.001)

    # stop the robot 
    robot.stop()

    # log leaving the function
    print("Leaving run to blackline", file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)

#. . . . . . .  .. . . . .  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
"""

might be untested

"""

def squareOnLine(stop, speed, target):
    print("In squareOnLine", file=stderr)

    # read the environment variable 'is_complete'
    is_complete = None
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])

    if 'Debugging' in os.environ:
        debugging = int(os.environ['Debugging'])
    # setting up program
    colourLeft_RLI = 0
    colourRight_RLI = 0
    lineFound = False
    #Turning on motor
    robot.drive(turn_rate=0,speed=speed)
    while True:
        #reading in the colour sensor values (reflected light intensity)
        colourLeft_RLI = colourLeft.reflection()
        colourRight_RLI = colourRight.reflection()
        # if the left Rli is smaller than the target/aim then turn to the right
        if colourLeft_RLI <= target:
            if debugging == True:
                print("ColourLeftRLI = {}".format(colourLeft_RLI), file = stderr)
            largeMotor_Left.run(-speed)
            largeMotor_Right.run(speed)
            lineFound = True #setting bool varisable for cancelling movment later on
            print('{} left found it'.format(colourLeft_RLI), file = stderr)

        # if the right Rli is smaller than the target/aim then turn to the left
        if colourRight_RLI <=target:
            if debugging == True:
                print("RightRLI = {}".format(colourRight_RLI), file = stderr)
            largeMotor_Left.run(speed)
            largeMotor_Right.run(-speed)
            lineFound = True #setting bool varisable for cancelling movment later on
            print('{} right found it'.format(colourRight_RLI), file = stderr)

        print('{} left, {} right'.format(colourLeft_RLI, colourRight_RLI), file = stderr)
    
        if colourLeft_RLI == colourRight_RLI and lineFound:
            break
        if stop():
            break

    # stop the robot 
    robot.stop()

    # log leaving the function
    print("Leaving square_on_line", file=stderr)
    # change 'is_complete' to the threadKey so the framework knows the function is complete
    is_complete = threadKey
    os.environ['IS_COMPLETE'] = str(is_complete)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#stopProcessing = False
#blackline_rotations(lambda:stopProcessing, 0, speed = 70, rotations = 20, sensor = 'LEFT', lineSide = 'LEFT', correction = 0.5)
#blackline_to_line(lambda: stopProcessing, 0, speed = 150, sensor = 'RIGHT', lineSide = 'RIGHT', correction = 0.8)
#squareOnLine(lambda:stopProcessing, speed=30, target=100)