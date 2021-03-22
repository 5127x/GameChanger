#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import ColorSensor, GyroSensor, Motor
from pybricks.parameters import Port, Button
from pybricks.media.ev3dev import SoundFile

# basic imports
import ujson
import threading
import time
from sys import stderr
import os


# import the functions 
from Functions_Completed.blackline_rotations import blackline_rotations
from Functions_Completed.blackline_to_line import blackline_to_line
from Functions_Completed.do_nothing import do_nothing
from Functions_Completed.gyro_current import gyro_current
from Functions_Completed.gyro_current_to_line import gyro_current_to_line
from Functions_Completed.gyro_target_to_line import gyro_target_to_line
from Functions_Completed.gyro_target import gyro_target
from Functions_Completed.gyro_turn_to_target import gyro_turn_to_target
from Functions_Completed.gyro_turning import gyro_turning
from Functions_Completed.motor_onForRotations import motor_onForRotations
from Functions_Completed.motor_onForSeconds import motor_onForSeconds
from Functions_Completed.off import off
from Functions_Completed.reset_gyro import reset_gyro
from Functions_Completed.reset_gyro_2 import reset_gyro_2
from Functions_Completed.recalibrate_gyro import recalibrate_gyro
from Functions_Completed.square_on_line import squareOnLine
from Functions_Completed.steering_rotations import steering_rotations
from Functions_Completed.steering_seconds import steering_seconds
from Functions_Completed.waiting import waiting
from play_sound import play_sound

# define the different motors
largeMotor_Right = Motor(Port.B)
largeMotor_Left = Motor(Port.C)
panel = Motor(Port.D)
print("Motors Connected", file = stderr)

# define the different sensors
gyro = GyroSensor(Port.S4)
colourRight = ColorSensor(Port.S2)
colourLeft = ColorSensor(Port.S3)
colourkey = ColorSensor(Port.S1)
print("Sensors Connected", file = stderr)

# define the brick
ev3 = EV3Brick()

# check the battery percentage 
current_battery = ev3.battery.voltage()
battery_percent = round(current_battery/9)
print("Current Battery Percent: {}%".format(battery_percent/10),file = stderr)
print("")

ev3.speaker.set_volume(100, which = '_all_')


# check if the key has been removed from the robot
def isKeyTaken(rProgram, gProgram, bProgram):  
    # read the colourkey sensor 
    rbgA = colourkey.rgb()
    # compare the current reading to the values shown when the key is inserted
    # rgb values are (12, 19, 27) when the slot is empty
    return abs(rbgA[0] - rProgram) > 5 and abs(rbgA[1] - gProgram) > 5 and abs(rbgA[2] - bProgram) > 5 

# calibrate the sensor's values for the different keys
def colourAttachment_values(): 
    # set a larger font 
    os.system('setfont Lat15-TerminusBold14') # os.system('setfont Lat15-TerminusBold32x16')  

    # print instructions and collect the rgb values for each key

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

    # collect the white value 
    #ev3.speaker.say('Insert white')
    print('Insert white')
    ev3.screen.print('Insert white')
    ev3.speaker.play_file(SoundFile.WHITE)
    while True:
        if Button.CENTER in ev3.buttons.pressed():
            white = colourkey.rgb()
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
    # wait a bit before the next key 
    time.sleep(.5)

    # collect the black value 
    # #ev3.speaker.say('Insert black')
    print('Insert black')
    ev3.screen.print('Insert black')
    ev3.speaker.play_file(SoundFile.BLACK)
    while True:
        if Button.CENTER in ev3.buttons.pressed():
            black = colourkey.rgb()
            break
    # wait a bit before the next key 
    time.sleep(.5)


    print('Finished!')
    ev3.screen.print('Finshed')
    ev3.speaker.play_file(SoundFile.GO)
    time.sleep(1)
    print("")

    # return the values for the different keys 
    attachment_values = [white, yellow, black, blue, green]
    return attachment_values

# launch actions using threads
def launchStep(stop, threadKey, action):
    # collect the name of the function from the information passed in 
    name = action["step"]

    # example of the code used to start a function
    ''' 
    if name == '': # (list of variables)
        print(name, file=stderr)
        thread = threading.Thread(target=, args=(stop, threadKey, variables))
        thread.start()
        return thread 
    '''

    # turns all the motors off without using brakes
    if name == 'off': # parameters ()
        print("Running off", file=stderr)
        thread = threading.Thread(target=off) 
        thread.start()
        return thread

    # wait until the key is removed at the end of a run
    if name == 'do_nothing': # parameters (stop, threadKey)
        print("Starting do_nothing", file= stderr)
        thread = threading.Thread(target = do_nothing, args = (stop, threadKey))
        thread.start()
        return thread

    # wait for a set amount of time
    if name == 'waiting': # parameters (stop, threadKey, seconds) 
        print("Starting waiting", file=stderr)
        seconds = float(action['seconds'])
        thread = threading.Thread(target=waiting, args=(stop, threadKey, seconds))
        thread.start()
        return thread

    # turn a single motor for a set amount of time 
    if name == 'motor_onForSeconds': # parameters (stop, threadKey, motor, speed, seconds)
        print("Starting motor_onForSeconds", file=stderr)
        motor = action.get('motor')
        speed = float(action['speed'])
        seconds = float(action['seconds'])
        if (motor == "largeMotor_Left"):
            motorToUse = largeMotor_Left
        if (motor == "largeMotor_Right"):
            motorToUse = largeMotor_Right
        if (motor == "panel"):
            motorToUse = panel
        if (motor == "extension"):
            motorToUse = motor 
        thread = threading.Thread(target=motor_onForSeconds, args=(stop, threadKey, motorToUse, speed, seconds))
        thread.start()
        return thread

    # turn a single motor for a set number of rotations 
    if name == 'motor_onForRotations': # parameters (stop, threadKey, motor, speed, rotations, gearRatio)
        print("Starting motor_onForRotations", file=stderr)
        motor = action['motor']
        speed = float(action['speed'])
        rotations = float(action['rotations'])
        gearRatio = float(action['gearRatio'])
        if (motor == "largeMotor_Left"):
            motorToUse = largeMotor_Left
        if (motor == "largeMotor_Right"):
            motorToUse = largeMotor_Right
        if (motor == "extension"):
            motorToUse = motor
        if motor == "panel":
            motorToUse = panel
        thread = threading.Thread(target=motor_onForRotations, args=(stop, threadKey, motorToUse, speed, rotations, gearRatio))
        thread.start()
        return thread

    # drive using a steering block for a set amount of time
    if name == 'steering_seconds': # parameters (stop, threadKey, speed, seconds, steering)
        print("Starting steering_seconds", file=stderr)
        speed = float(action['speed'])
        seconds = float(action['seconds'])
        steering = float(action['steering'])
        thread = threading.Thread(target=steering_seconds, args= (stop, threadKey, speed, seconds, steering))
        thread.start()
        return thread

    # drive using a steering block for a set number of rotations 
    if name == 'steering_rotations': # parameters (stop, threadKey, speed, rotations, steering)
        print("Starting steering_rotations", file=stderr)
        speed = float(action['speed'])
        rotations = float(action['rotations'])
        steering = float(action['steering'])
        thread = threading.Thread(target=steering_rotations, args=(stop, threadKey, speed, rotations, steering))
        thread.start()
        return thread
    
    if name == 'squareOnLine': # parameters (stop, threadKey, speed, sensor, correction)
        print("Starting square_on_line", file=stderr)
        speed = float(action['speed'])
        thread = threading.Thread(target=gyro_current_to_line, args=(stop, threadKey, speed))
        thread.start()
        return thread

    # follow a black line for a set number of rotations 
    if name == 'blackline_rotations': # parameters (stop, threadKey, speed, rotations, sensor, lineSide, correction)
        print("Starting blackline_rotations", file=stderr)
        speed = float(action['speed'])
        rotations = float(action['rotations'])
        sensor = action['sensor']
        lineSide = action['lineSide']
        correction = float(action['correction'])
        thread = threading.Thread(target = blackline_rotations, args=(stop, threadKey, speed, rotations, sensor, lineSide, correction))
        thread.start()
        return thread

    # follow a black line until the opposite sensor sees another line
    if name == 'blackline_to_line': # parameters (stop, threadKey, speed, sensor, lineSide, correction)
        print("Starting blackline_to_line", file = stderr)
        speed = float(action['speed'])
        sensor = action['sensor']
        lineSide = action['lineSide']
        correction = float(action['correction'])
        thread = threading.Thread(target = blackline_to_line, args=(stop, threadKey, speed, sensor, lineSide, correction))
        thread.start()
        return thread


    # recalibrates the gyro 
    if name == 'recalibrate_gyro': # parameters (stop, threadKey)
        print("Starting recalibrate_gyro", file=stderr)
        thread = threading.Thread(target=recalibrate_gyro, args=(stop, threadKey))
        thread.start()
        return thread

    # resets the gyro before a run
    if name == 'reset_gyro': # parameters (stop, threadKey)
        print("Starting reset_gyro", file=stderr)
        thread = threading.Thread(target=reset_gyro, args=(stop,threadKey))
        thread.start()
        return thread

    if name == 'reset_gyro_2': # parameters (stop, threadKey)
        print("Starting reset_gyro 2", file=stderr)
        thread = threading.Thread(target=reset_gyro_2, args=(stop,threadKey))
        thread.start()
        return thread

    # use the gyro to drive in a straight line facing the direction it currently faces for a set number of rotations
    if name == 'gyro_current': # parameters (stop, threadKey, speed, rotations, correction)
        print("Starting gyro_current", file=stderr)
        speed = float(action['speed'])
        rotations = float(action['rotations'])
        correction = float(action['correction'])
        thread = threading.Thread(target=gyro_current, args=(stop, threadKey, speed, rotations, correction))
        thread.start()
        return thread

    # use the gyro to drive in a straight line facing the direction it currently faces until the sensor sees a line
    if name == 'gyro_current_to_line': # parameters (stop, threadKey, speed, sensor, correction)
        print("Starting gyro_current_to_line", file=stderr)
        speed = float(action['speed'])
        sensor = action['sensor']
        correction = float(action['correction'])
        thread = threading.Thread(target=gyro_current_to_line, args=(stop, threadKey, speed, sensor, correction))
        thread.start()
        return thread

    # use the gyro to drive in a straight line facing the given direction for a set number of rotations 
    if name == 'gyro_target': # parameters (stop, threadKey, speed, rotations, target, correction)
        print("Starting gyro_target", file=stderr)
        speed = float(action['speed'])
        rotations = float(action['rotations'])
        target = float(action['target'])
        correction = float(action['correction'])
        thread = threading.Thread(target=gyro_target, args=(stop, threadKey, speed, rotations, target, correction))
        thread.start()
        return thread

    # use the gyro to drive in a straight line facing the given direction until the sensor sees a line
    if name == 'gyro_target_to_line': # parameters (stop, threadKey, speed, sensor, target, correction)
        print("Starting gyro_target_to_line", file=stderr)
        speed = float(action['speed'])
        sensor = action['sensor']
        target = float(action['target'])
        correction = float(action['correction'])
        thread = threading.Thread(target=gyro_target_to_line, args=(stop, threadKey, speed, sensor, target, correction))
        thread.start()
        return thread

    # turn using the gyro to face a given angle
    if name == 'gyro_turn_to_target': # parameters (stop, threadKey, speed, degrees)
        print("Starting gyro_turn_to_target", file=stderr)
        speed = float(action['speed'])
        degrees = float(action['degrees'])
        thread = threading.Thread(target = gyro_turn_to_target, args=(stop, threadKey, speed, degrees))
        thread.start()
        return thread

    # turn a given angle to either side using the gyro
    if name == 'gyro_turning': # parameters (stop, threadKey, speed, degrees)
        print("Starting gyro_turning", file=stderr)
        speed = float(action['speed'])
        degrees = float(action['degrees'])
        thread = threading.Thread(target = gyro_turning, args=(stop, threadKey, speed, degrees))
        thread.start()
        return thread

    # play a sound file 
    if name == 'play_sound': # parameters (sound_file_name)
        print("Starting play_sound", file=stderr)
        sound_file_name = action['sound_file_name']
        thread = threading.Thread(target= play_sound, args=(sound_file_name, ))
        thread.start()
        return thread

# set is_complete as an enviroment variable 
is_complete = 0
os.environ['IS_COMPLETE'] = str(is_complete)

# main section of the program
def main():
    # create dictionaries and variables
    threadPool = {}
    stopProcessing = False
    threadKey = 1

    # collect the values of the coloured keys 
    attachment_values = colourAttachment_values()

    # open and read the overall JSON file 
    with open('overall_programming.json') as f:
        parsed = ujson.load(f)
        programsList = parsed["programs"]

        # loop until the program is completely stopped 
        while True:
            # reset stopProcessing each repetition
            stopProcessing = False

            # reset variables for a new run 
            threadPool = {}
            is_complete = 0
            os.environ['IS_COMPLETE'] = str(is_complete)

            # collect the raw rgb light values from colourkey sensor 
            rgb = colourkey.rgb()

            for program in programsList:
                # compare the saved readings of the coloured keys for each program to the current reading of the sensor 
                programName = program["name"]
                colourValue = int(program["colourValue"])
                
                # reading the colour
                colourProgram = attachment_values[colourValue]
                rProgram = colourProgram[0]
                gProgram = colourProgram[1]
                bProgram = colourProgram[2]
                rColourSensor = rgb[0]
                gColourSensor = rgb[1]
                bColourSensor = rgb[2]

                # compare the sets of values: if the values match, run the corresponding program
                if abs(rColourSensor - rProgram) < 4 and abs(gColourSensor - gProgram) < 4 and abs(bColourSensor - bProgram) < 4:
                    # read the relevant program JSON file 
                    fileName = program["fileName"]
                    print(fileName, file=stderr)

                    # calculating in the current value
                    os.environ['gyro_reading_env_var'] = gyro.angle()
                    print("OS Gyro Enviroment Variable read", file = stderr)

                    with open(fileName) as f:
                        parsed = ujson.load(f)
                        steps = parsed["steps"]
                        
                        ev3.speaker.play_file(SoundFile.CONFIRM)
                        # run each step individually unless they are run in parallel
                        for step in steps:
                            action = step["step"]
                            print ('{} {}'.format(action, step), file = stderr)

                            # loop through actions that should be run in parallel and run each one 
                            if action == 'launchInParallel':
                                subSteps = step["subSteps"]
                                for subStep in subSteps:
                                    print('subStep {}'.format(subStep))
                                    thread = launchStep(lambda:stopProcessing, threadKey, subStep)
                                    threadPool[threadKey] = thread
                                    threadKey = threadKey+1  

                            # run each action that isn't run in parrallel idividually
                            else:
                                thread = launchStep(lambda:stopProcessing, threadKey, step)
                                threadPool[threadKey] = thread
                                threadKey = threadKey+1  

                            while not stopProcessing:
                                # if there are no threads running and the run hasn't been stopped, start the next action
                                if not threadPool:
                                    break
                                
                                # remove any completed threads from the threadPool
                                is_complete = int(os.environ['IS_COMPLETE'])
                                if is_complete != 0: 
                                    del threadPool[is_complete]
                                    is_complete = 0
                                    os.environ['IS_COMPLETE'] = str(is_complete)
                                    # log that a thread was deleted and which threads are left in the threadPool
                                    print("deleted a thread", file=stderr)
                                    print("threadpool {}".format(threadPool), file=stderr)
                                    print('')
                                
                                # if the key is removed then stop everything by raising the 'stopProcessing' flag
                                if isKeyTaken(rProgram, gProgram, bProgram):
                                    stopProcessing = True
                                    break

                            # if the 'stopProcessing' flag has been set then finish the whole loop
                            if stopProcessing:
                                threadPool.clear()
                                # turn off the motors without brakes so they dont lock up
                                try:
                                    largeMotor_Left.stop()
                                    largeMotor_Right.stop()
                                    panel.stop()
                                    print('motors stopped')
                                except:
                                    print("didnt stop")
                                
                                break

#play sound to know that the framework is about to run. (helps makek you aware that the program is about to start)
ev3.speaker.play_file(SoundFile.CONFIRM)

main()