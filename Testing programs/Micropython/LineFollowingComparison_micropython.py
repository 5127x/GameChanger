#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase

colourLeft = ColorSensor(Port.S2)
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

ev3 = EV3Brick()
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

target_RLI = 45 
def line_following(speed_value, correction):
    while True:
        current_RLI = colourLeft.reflection()
        error = current_RLI - target_RLI
        steering = (error * correction)#error * correction
        robot.drive(speed_value,steering)

line_following(speed_value = 600, correction = 0.2)

#____________
# This program was created on the 10/8/2020 it's purpose is to compare with it's twin ev3dev program 
# (LineFollowingComparison_ev3dev.py)

# The 2 programs were created as similar to each other as popular including the imports however some
#adjustments had to be made as the syntax for the different langauges are different
