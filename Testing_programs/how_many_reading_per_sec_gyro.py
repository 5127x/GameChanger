#!/usr/bin/env pybricks-micropython
# - Micropython -
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import GyroSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
import time
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# define the motors, sensors and the brick

gyro = GyroSensor(Port.S4)
ev3 = EV3Brick()

Current_Counting_Time = 0

start_time = time.time()
while time.time() < 10:
    current_gyro_reading=gyro.angle()
    Current_Counting_Time = Current_Counting_Time +1
    if time.time() > 10:
        break

print("It read {} many times", Current_Counting_Time)