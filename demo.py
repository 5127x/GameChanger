#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import ColorSensor, GyroSensor, Motor
from pybricks.parameters import Port
from pybricks.media.ev3dev import SoundFile
from Functions_Completed.waiting import waiting
import os
from sys import stderr
largeMotor_Right = Motor(Port.B)
largeMotor_Left = Motor(Port.C)
panel = Motor(Port.D)
print("Motors Connected", file = stderr)

gyro = GyroSensor(Port.S1)
colourRight = ColorSensor(Port.S2)
colourLeft = ColorSensor(Port.S3)
colourkey = ColorSensor(Port.S4)
print("Sensors Connected", file = stderr)


ev3 = EV3Brick()

#test for gyro creep
x=False 
while True: 
    print(gyro.angle())
    waiting(lambda:x, 0, 0.5)