#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import ColorSensor, GyroSensor, Motor
from pybricks.parameters import Port
from pybricks.media.ev3dev import SoundFile
'''
from ev3dev2.motor import MoveSteering, MoveTank, MediumMotor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, GyroSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.button import Button'''
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
from Functions_Completed.gyro_target_to_line import gyro_target_to_line
from Functions_Completed.gyro_target import gyro_target
from Functions_Completed.gyro_turn_to_target import gyro_turn_to_target
from Functions_Completed.gyro_turning import gyro_turning
from Functions_Completed.motor_onForRotations import motor_onForRotations
from Functions_Completed.motor_onForSeconds import motor_onForSeconds
from Functions_Completed.off import off
from Functions_Completed.reset_gyro import reset_gyro
from Functions_Completed.steering_rotations import steering_rotations
from Functions_Completed.square_onLine import square_onLine
from Functions_Completed.steering_seconds import steering_seconds
from Functions_Completed.waiting import waiting

# define the different sensors, motors and motor blocks
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
current_battery = ev3.battery.voltage()
battery_percent = round(current_battery/9)
print("Current Battery Percent: {}%".format(battery_percent/10),file = stderr)
print("")

''' # dont know what the new python version is 
steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C) 
tank_block = MoveTank(OUTPUT_B, OUTPUT_C)
'''

# check if the key has been removed
def isKeyTaken(rProgram, gProgram, bProgram): 
    # return True if the key was removed and stop the motors 
    rbgA = colourkey.rgb()
    # compare the current values to the values shown when the key is inserted   
    # (rgb values are 50, 62, 57 when the slot is empty)
    return abs(rbgA[0] - rProgram) > 4 and abs(rbgA[1] - gProgram) > 4 and abs(rbgA[2] - bProgram) > 4 #returns which run to run

# calibrate the colourAttachment values for the different keys
def colourAttachment_values(): 
    stop = False
    # set a larger font 
    os.system('setfont Lat15-TerminusBold14') # os.system('setfont Lat15-TerminusBold32x16')  

    # print instructions and collect the rgb values for each key
    # NOW ON SCALE OF 1-100 INSTEAD OF 1-255
    print('Insert white', file=stderr)
    print('Insert white')
    time.sleep(5)
    white = colourkey.rgb()
    print('Next.')

    print('Insert yellow', file=stderr)
    print('Insert yellow')
    time.sleep(5)
    yellow = colourkey.rgb()
    print('Next.')

    print('Insert red', file=stderr)
    print('Insert red')
    time.sleep(5)
    red = colourkey.rgb()
    print('Next.')

    print('Insert blue', file=stderr)
    print('Insert blue')
    time.sleep(5)
    blue = colourkey.rgb()
    print('Next.')

    print('Insert green', file=stderr)
    print('Insert green')
    time.sleep(5)
    green = colourkey.rgb()
    print('Done!')
    time.sleep(3)
    # return the values for the different keys
    attachment_values = [white, yellow, red, blue, green]
    return attachment_values

# launch actions using threads
def launchStep(stop, threadKey, action):
    
    if 'IS_COMPLETE' in os.environ:
        is_complete = int(os.environ['IS_COMPLETE'])
    
    # compare the 'name' to the functions and start a thread with the matching function
    # return the thread to be added to the thre6adPool
    name = action["step"]

    ''' 
   if name == '': # (list of variables)
        print(name, file=stderr)
        thread = threading.Thread(target=, args=(stop, threadKey, variables))
        thread.start()
        return thread
    
    '''
    
    if name == 'blackline_rotations':# (stop, speed, rotations, sensor, lineSide,correction)
        print("Starting BlackLine_rotations", file=stderr)
        speed = float(action['speed'])
        rotations = float(action['rotations'])
        sensor = action['sensor']
        lineSide = action['lineSide']
        correction = float(action['correction'])
        thread = threading.Thread(target = blackline_rotations, args=(stop,threadKey, speed, rotations, sensor, lineSide,correction))
        thread.start()
        return thread

    if name == 'blackline_to_line': #stop, speed, sensor, lineSide, correction
        print("Starting blackline_to_line", file = stderr)
        speed = float(action['speed'])
        sensor = action['sensor']
        lineSide = action['lineSide']
        correction = float(action['correction'])
        thread = threading.Thread(target = blackline_to_line, args=(stop, threadKey, speed, sensor, lineSide, correction))
        thread.start()
        return thread

    if name == 'do_nothing': # (stop)
        print("do_nothing", file= stderr)
        thread = threading.Thread(target=Do_nothing, args=(stop,threadKey))
        thread.start()
        return thread

    if name == 'gyro_current': # (stop, speed, rotations, correction)
        print("Starting gyro_current", file=stderr)
        speed = float(action['speed'])
        rotations = float(action['rotations'])
        correction = float(action['correction'])
        thread = threading.Thread(target=gyro_current, args=(stop,threadKey, speed, rotations, correction))
        thread.start()
        return thread

    if name == 'gyro_target_to_line': # (stop, speed, rotations, target, whiteOrBlack)
        print("Starting gyro_target_to_line", file=stderr)
        speed = float(action['speed'])
        rotations = float(action['rotations'])
        target = float(action['target'])
        whiteOrBlack = action['whiteOrBlack']
        thread = threading.Thread(target=gyro_target_to_line, args=(stop, threadKey, speed, rotations, target, whiteOrBlack))
        thread.start()
        return thread

    if name == 'gyro_target': # (stop, speed, rotations, target, correction)
        print("Starting gyro_target", file=stderr)
        speed = float(action['speed'])
        rotations = float(action['rotations'])
        target = float(action['target'])
        correction = float(action['correction'])
        thread = threading.Thread(target=gyro_target, args=(stop,threadKey, speed, rotations, target, correction))
        thread.start()
        return thread

    if name == 'gyro_turn_to_target': # (stop, speed, degrees)
        print("Starting gyro_turn_to_target", file=stderr)
        speed = float(action['speed'])
        degrees = float(action['degrees'])
        thread = threading.Thread(target = gyro_turn_to_target, args=(stop, threadKey, speed, degrees))
        thread.start()
        return thread

    if name == 'gyro_turning': # (stop, speed, degrees)
        print("Starting gyro_turning", file=stderr)
        speed = float(action['speed'])
        degrees = float(action['degrees'])
        thread = threading.Thread(target = gyro_turning, args=(stop, threadKey, speed, degrees))
        thread.start()
        return thread

    if name == 'motor_onForRotations': # (stop, motor, speed, rotations, gearRatio)
        print("Starting Motor_onForRotations", file=stderr)
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

    if name == 'motor_onForSeconds': # (stop, motor, speed, rotations)
        print("Starting motor_onForSeconds", file=stderr)
        motor = action.get('motor')
        speed = float(action['speed'])
        seconds = float(action['seconds'])
        if (motor == "largeMotor_Left"):
            motmotorToUse = largeMotor_Left
        if (motor == "largeMotor_Right"):
            motorToUse = largeMotor_Right
        if (motor == "panel"):
            motorToUse = panel
        if (motor == "extramotor"):
            motorToUse = extramotor
        thread = threading.Thread(target=motor_onForSeconds, args=(stop,threadKey, motorToUse, speed, seconds))
        thread.start()
        return thread
 
    if name == 'off': # ()
        print("Motors off", file=stderr)
        thread = threading.Thread(target=off, args=(threadKey,)) 
        thread.start()
        return thread


    if name == 'reset_gyro': # ()
        print("Starting Reset_gyro", file=stderr)
        thread = threading.Thread(target=reset_gyro, args=(threadKey,))
        thread.start()
        return thread

    if name == 'square_onLine': # (stop, speed, target)
        print("Starting square_onLine", file=stderr)
        speed = float(action['speed'])
        target = float(action['target'])
        thread = threading.Thread(target=square_onLine, args=(stop, speed, target))
        thread.start()
        return thread
    

    if name == 'steering_rotations': # (stop, speed, rotations, steering)
        print("Starting Steering_rotations", file=stderr)
        speed = float(action['speed'])
        rotations = float(action['rotations'])
        steering = float(action['steering'])
        thread = threading.Thread(target=steering_rotations, args=(stop,threadKey, speed, rotations, steering))
        thread.start()
        return thread

    if name == 'steering_seconds': # (stop, speed, seconds, steering)
        print("Starting Steering_seconds", file=stderr)
        speed = float(action['speed'])
        seconds = float(action['seconds'])
        steering = float(action['steering'])
        thread = threading.Thread(target=steering_seconds, args= (stop, threadKey, speed, seconds, steering))
        thread.start()
        return thread

    if name == 'waiting': # (stop, seconds) 
        print("Starting waiting", file=stderr)
        seconds = float(action['seconds'])
        thread = threading.Thread(target=waiting, args=(stop, threadKey, seconds))
        thread.start()
        return thread


is_complete = 0
os.environ['IS_COMPLETE'] = str(is_complete)
# main section of the program
def main():
    # create dictionaries and variables
    threadPool = {}
    stopProcessing = False
    threadKey = 1
    attachment_values = colourAttachment_values()
    # open and read the overall XML file 
    with open('overall_programming.json') as f:
        parsed = ujson.load(f)
        programsList = parsed["programs"]
    
        while True:
            # reset stopProcessing each repetition
            stopProcessing = False
            # collect the raw rgb light values from colourAttachment and the overall XML file
            rgb = colourkey.rgb()
            
            # FUCKING FIX THIS 
            for program in programsList:
                #program = programsList[x]
                programName = program["name"]
                colourValue = int(program["colourValue"])
                
                # use the calibrated values in comparison 
                colourProgram = attachment_values[colourValue]
                rProgram = colourProgram[0]
                gProgram = colourProgram[1]
                bProgram = colourProgram[2]
                rColourSensor = rgb[0]
                gColourSensor = rgb[1]
                bColourSensor = rgb[2]
                # compare the sets of values
                # if the values match, run the corresponding program
                if abs(rColourSensor - rProgram) < 4 and abs(gColourSensor - gProgram) < 4 and abs(bColourSensor - bProgram) < 4:
                    #mediumMotor.reset 

                    # read the relevant program XML
                    fileName = program["fileName"]
                    print(fileName, file=stderr)
                    with open(fileName) as f:
                        parsed = ujson.load(f)
                        steps = parsed["steps"]
                        
                        # run each step individually unless they are run in parallel
                        for step in steps:
                            action = step["step"]
                            print ('{} {}'.format(action, step), file = stderr)
                            # loop through actions that should be run in parallel
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
                                # if there are no threads running start the next action
                                if not threadPool:
                                    break
                                
                                # remove any completed threads from the pool
                                is_complete = int(os.environ['IS_COMPLETE'])
                                if is_complete != 0: 
                                    del threadPool[is_complete]
                                    is_complete = 0
                                    os.environ['IS_COMPLETE'] = str(is_complete)
                                    print("deleted thread", file=stderr)
                                    print("threadpool {}".format(threadPool), file=stderr)
                                    print('')
                                
                                # if the robot has been lifted or the key removed then stop everything
                                if isKeyTaken(rProgram, gProgram, bProgram):
                                    stopProcessing = True
                                    break

                            # if the 'stopProcessing' flag has been set then finish the whole loop
                            if stopProcessing:
                                #off()
                                try:
                                    largeMotor_Left.stop()
                                    largeMotor_Right.stop()
                                    panel.stop()
                                    print('motors stopped')
                                except:
                                    print("didnt stop")
                                
                                break

main()