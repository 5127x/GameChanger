#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import ColorSensor, GyroSensor, Motor
from pybricks.parameters import Port
from pybricks.media.ev3dev import SoundFile

ev3 = EV3Brick()

def play_sound (sound_file_name): # sound_file_name is a str 
    ev3.speaker.set_volume(100, which = '_all_')
    ev3.speaker.play_file(sound_file_name)

#play_sound('test.wav')