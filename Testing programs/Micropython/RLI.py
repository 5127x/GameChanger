#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase


ev3 = EV3Brick()
colourLeft = ColorSensor(Port.S2)

#steering_drive = steering.drive(Motor(Port.B), Motor(Port.C))

# Initialize the motors.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

#_________________________________________________________________________________________________________________________________

def RLI_testing():
    x=0
    start_time = time.time()
    while time.time() < start_time + 1:
        RLI = colourLeft.reflected_light_intensity
        x = x+1
    print(x, file=stderr)