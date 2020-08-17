#!/usr/bin/env python3
from ev3dev2.motor import MoveSteering, LargeMotor,OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_2
colourLeft = ColorSensor(INPUT_2)
largeMotor_Left= LargeMotor(OUTPUT_B)
largeMotor_Right= LargeMotor(OUTPUT_C)

target_RLI = 45
steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)

def line_following(speed_value,correction):
    while True:
        current_RLI = colourLeft.reflected_light_intensity
        error = current_RLI - target_RLI
        steering = (error * correction)#error * correction
        steering_drive.on(speed=speed_value,steering = steering)

line_following(speed_value =65, correction = .2)

#____________
# This program was created on the 10/8/2020 it's purpose is to compare with it's twin micropython program 
# (LineFollowingComparison_micropython.py)

# The 2 programs were created as similar to each other as popular including the imports however some
# adjustments had to be made as the syntax for the different langauges are different

