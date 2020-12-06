#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import ColorSensor, GyroSensor, Motor
from pybricks.parameters import Port, Button
from pybricks.media.ev3dev import SoundFile
#from Functions_Completed.waiting import waiting
import os
from sys import stderr
import time 

largeMotor_Right = Motor(Port.B)
largeMotor_Left = Motor(Port.C)
panel = Motor(Port.D)
print("Motors Connected", file = stderr)

gyro = GyroSensor(Port.S4)
colourRight = ColorSensor(Port.S2)
colourLeft = ColorSensor(Port.S3)
colourkey = ColorSensor(Port.S1)
print("Sensors Connected", file = stderr)


ev3 = EV3Brick()
'''
#test for gyro creep
while True:
    time.sleep(0.5)
    rli = colourRight.reflection()
    print(rli, file=stderr)

time.sleep(5)


x=False 

while True: 
    print(gyro.angle())
    waiting(lambda:x, 0, 0.5)
'''

'''
rgbWhite = colourkey.rgb()
print("NEXT", file=stderr)
waiting(lambda:x, 0, 4)
rgbYellow = colourkey.rgb()
print("NEXT", file=stderr)
waiting(lambda:x, 0, 4)
rgbRed = colourkey.rgb()
print("NEXT", file=stderr)
waiting(lambda:x, 0, 4)
rgbBlue = colourkey.rgb()
print("NEXT", file=stderr)
waiting(lambda:x, 0, 4)
rgbEmpty = colourkey.rgb()
print("NEXT", file=stderr)
waiting(lambda:x, 0, 4)
rgbGreen = colourkey.rgb()
print("DONE", file=stderr)

print(rgbWhite, file=stderr)
print(rgbYellow, file=stderr)
print(rgbRed, file=stderr)
print(rgbBlue, file=stderr)
print(rgbEmpty, file=stderr)
print(rgbGreen, file=stderr)
# 1. white
# 2. yellow
# 3. red 
# 4. blue
'''

'''
(69, 99, 100) white 
(61, 56, 16) yellow
(44, 13, 9) red
(6, 24, 63) blue
(12, 19, 27) empty
(6, 33, 14) green
'''

# MIGHT WORK BUT HASNT BEEN TESTEDs

# calibrate the sensor's values for the different keys
def colourAttachment_values(): 
    # set a larger font 
    os.system('setfont Lat15-TerminusBold14') # os.system('setfont Lat15-TerminusBold32x16')  
    
    while True:
        if Button.DOWN in ev3.buttons.pressed():
            ValueFile = open("ValueFile.txt","r")

            white = ValueFile.readline()
            yellow = ValueFile.readline()
            red = ValueFile.readline()
            blue = ValueFile.readline()
            green = ValueFile.readline()

            ValueFile.close()
            break

        elif Button.CENTER in ev3.buttons.pressed():
            time.sleep(.5)

            # collect the white value 
            print('Insert white')
            ev3.screen.print('Insert white')
            while True:
                if Button.CENTER in ev3.buttons.pressed():
                    white = colourkey.rgb()
                    break
            # wait a bit before the next key 
            time.sleep(.5)

            # collect the yellow value 
            print('Insert yellow')
            ev3.screen.print('Insert yellow')
            while True:
                if Button.CENTER in ev3.buttons.pressed():
                    yellow = colourkey.rgb()
                    break
            # wait a bit before the next key 
            time.sleep(.5)

            # collect the red value 
            print('Insert red')
            ev3.screen.print('Insert red')
            while True:
                if Button.CENTER in ev3.buttons.pressed():
                    red = colourkey.rgb()
                    break
            # wait a bit before the next key 
            time.sleep(.5)

            # collect the blue value 
            print('Insert blue')
            ev3.screen.print('Insert blue')
            while True:
                if Button.CENTER in ev3.buttons.pressed():
                    blue = colourkey.rgb()
                    break
            # wait a bit before the next key 
            time.sleep(.5)

            # collect the green value 
            print('Insert green')
            ev3.screen.print('Insert green')
            while True:
                if Button.CENTER in ev3.buttons.pressed():
                    green = colourkey.rgb()
                    break
            
            # finished 
            print('Finished!')
            ev3.screen.print('Finshed')
            time.sleep(1)
            print("")

            # return the values for the different keys
            
            ValueFile = open("ValueFile.txt","w")
            ValueFile.write(str(white[0])) 
            ValueFile.write(", ")
            ValueFile.write(str(white[1])) 
            ValueFile.write(", ")
            ValueFile.write(str(white[2])) 
            ValueFile.write("\n")

            ValueFile.write(str(yellow[0])) 
            ValueFile.write(", ")
            ValueFile.write(str(yellow[1])) 
            ValueFile.write(", ")
            ValueFile.write(str(yellow[2]))  
            ValueFile.write("\n")

            ValueFile.write(str(red[0])) 
            ValueFile.write(", ")
            ValueFile.write(str(red[1])) 
            ValueFile.write(", ")
            ValueFile.write(str(red[2])) 
            ValueFile.write("\n")
            
            ValueFile.write(str(blue[0])) 
            ValueFile.write(", ")
            ValueFile.write(str(blue[1])) 
            ValueFile.write(", ")
            ValueFile.write(str(blue[2])) 
            ValueFile.write("\n")

            ValueFile.write(str(green[0])) 
            ValueFile.write(", ")
            ValueFile.write(str(green[1])) 
            ValueFile.write(", ")
            ValueFile.write(str(green[2])) 

            ValueFile.close()
            break 
    attachment_values = [white, yellow, red, blue, green]

    return attachment_values


print(colourAttachment_values())

ValueFile = open("ValueFile.txt","r")

Vwhite = ValueFile.readline()
Vyellow = ValueFile.readline()
Vred = ValueFile.readline()
Vblue = ValueFile.readline()
Vgreen = ValueFile.readline()

ValueFile.close()

l = Vwhite.split(",")
white = []
for i in l:
    white.append(int(i))
print(white)

l = Vyellow.split(",")
yellow = []
for i in l:
    yellow.append(int(i))
print(yellow)

l = Vred.split(",")
red = []
for i in l:
    red.append(int(i))
print(red)

l = Vblue.split(",")
blue = []
for i in l:
    blue.append(int(i))
print(blue)

l = Vgreen.split(",")
green = []
for i in l:
    green.append(int(i))
print(green)