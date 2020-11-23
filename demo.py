#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import ColorSensor, GyroSensor, Motor
from pybricks.parameters import Port, Button
from pybricks.media.ev3dev import SoundFile
from Functions_Completed.waiting import waiting
import os
from sys import stderr
import time 
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

            white = ValueFile.readline([0])
            yellow = ValueFile.readline([1])
            red = ValueFile.readline([2])
            blue = ValueFile.readline([3])
            green = ValueFile.readline([4])

            ValueFile.close()
            break

        elif Button.CENTER in ev3.buttons.pressed():
            # collect the white value 
            # ev3.speaker.say('Insert white')
            
            print('Insert white')
            ev3.screen.print('Insert white')
            ev3.speaker.play_file(SoundFile.WHITE)
            while True:
                if Button.CENTER in ev3.buttons.pressed():
                    white = colourkey.rgb()
                    break
            # wait a bit before the next key 
            time.sleep(.5)

            # collect the yellow value 
            #ev3.speaker.say('Insert yellow')
            print('Insert yellow')
            ev3.screen.print('Insert yellow')
            ev3.speaker.play_file(SoundFile.YELLOW)
            while True:
                if Button.CENTER in ev3.buttons.pressed():
                    yellow = colourkey.rgb()
                    break
            # wait a bit before the next key 
            time.sleep(.5)

            # collect the red value 
            # #ev3.speaker.say('Insert red')
            print('Insert red')
            ev3.screen.print('Insert red')
            ev3.speaker.play_file(SoundFile.RED)
            while True:
                if Button.CENTER in ev3.buttons.pressed():
                    red = colourkey.rgb()
                    break
            # wait a bit before the next key 
            time.sleep(.5)

            # collect the blue value 
            #ev3.speaker.say('Insert blue')
            print('Insert blue')
            ev3.screen.print('Insert blue')
            ev3.speaker.play_file(SoundFile.BLUE)
            while True:
                if Button.CENTER in ev3.buttons.pressed():
                    blue = colourkey.rgb()
                    break
            # wait a bit before the next key 
            time.sleep(.5)

            # collect the green value 
            #ev3.speaker.say('Insert green')
            print('Insert green')
            ev3.screen.print('Insert green')
            ev3.speaker.play_file(SoundFile.GREEN)
            while True:
                if Button.CENTER in ev3.buttons.pressed():
                    green = colourkey.rgb()
                    break
            
            # finished 
            print('Finished!')
            ev3.screen.print('Finshed')
            ev3.speaker.play_file(SoundFile.GO)
            time.sleep(1)
            print("")

            # return the values for the different keys
            
            ValueFile = open("ValueFile.txt","w")
            ValueFile.write(white) 
            ValueFile.write(yellow) 
            ValueFile.write(red) 
            ValueFile.write(blue) 
            ValueFile.write(green) 
            ValueFile.close()
            break 
    attachment_values = [white, yellow, red, blue, green]
    return attachment_values


colourAttachment_values()