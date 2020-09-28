'''

steering_seconds.py
steering_rotations.py

reset_gyro.py
gyro_target.py
gyro_current.py
gyro_target_to_line.py
gyro_turning.py

blackline_rotations.py
blackline_to_line.py

off.py
do_nothing.py
waiting.py

//{"step": "blackline_to_line", "speed": "300", "sensor":"LEFT", "lineSide":"RIGHT", "correction":"0.2"}


#!/usr/bin/env pybricks-micropython
# - Micropython (new) -
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor, Gyro
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase

largeMotor_Right = Motor(Port.B)
largeMotor_Left = Motor(Port.C)
panel = Motor(Port.D)

gyro = ColorSensor(Port.S1)
colourRight = ColorSensor(Port.S2)
colourLeft = ColorSensor(Port.S3)
colourkey = ColorSensor(Port.S4)


ev3 = EV3Brick()
robot = DriveBase(left_motor, right_motor, wheel_diameter=62, axle_track=104)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#___________________________

#!/usr/bin/env python3
# - Ev3Dev (old) -
from ev3dev2.motor import MoveSteering, LargeMotor,OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4

largeMotor_Right= LargeMotor(OUTPUT_B)
largeMotor_Left= LargeMotor(OUTPUT_C)
panel= LargeMotor(OUTPUT_D)

gyro = GyroSensor(INPUT_1)
colourRight = ColorSensor(INPUT_2)
colourLeft = ColorSensor(INPUT_3)
colourkey = ColorSensor(INPUT_4)

'''