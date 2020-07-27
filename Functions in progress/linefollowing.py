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

#________________________________________________________________________________________________________________________
def testing_blackline (correction, speed):#
    while True:
        cur_RLI = colourLeft.reflected_light_intensity
        error = cur_RLI - 40
        steering = error * correction
        robot.drive(speed, steering) # Steering Block||old syntax steering_drive.on(speed,steering)


testing_blackline (0.5, 5)
'''
#!/usr/bin/env pybricks-micropython

import time
from sys import stderr
ev3 = EV3Brick()
colourLeft = ColorSensor(Port.S2)
def RLI_testing2():
    x=0
    start_time = time.time()
    while time.time() < start_time + 1:
        RLI = colourLeft.reflection()
        x = x+1
    print(x, file=stderr) '''

#27/7/20 | 27th July 2020