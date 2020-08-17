#!/usr/bin/env python3
#11.8.20 Speed_Testing_ev3dev.py -- > Speed_Testing_micropython.py

from ev3dev2.motor import MoveSteering, LargeMotor,OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_2
colourLeft = ColorSensor(INPUT_2)
largeMotor_Left= LargeMotor(OUTPUT_B)
largeMotor_Right= LargeMotor(OUTPUT_C)

def straight_line(speed_value):
    while True:
        steering_drive.on(speed=speed_value,steering = 0)

straight_line(speed_value = 5)