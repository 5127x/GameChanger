#!/usr/bin/env pybricks-micropython
#11.8.20 Speed_Testing_ev3dev.py -- > Speed_Testing_micropython.py


from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase

colourLeft = ColorSensor(Port.S2)
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

ev3 = EV3Brick()
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

def line_following(speed_value):
    while True:
        robot.drive(speed_value,0)

line_following(speed_value = 0)