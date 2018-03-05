#!/usr/bin/env python

import RPi.GPIO as GPIO
import sys, termios, tty, os, time, select
from subprocess import Popen
from PIL import Image

GPIO.setmode(GPIO.BCM)

GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
##GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

img = Image.open('scnshot.png')
video = "Reg.avi"
video1 = "TwoColors.avi"
video2 = "VideoBrief.avi"
last_state1= False
last_state2 = False
input_state1 = False
input_state2 = False
player = False
quit_video = False
character = None
killPause = False
kill = False
killPrime = False

##def getch():
##    fd = sys.stdin.fileno()
##    old_settings = termios.tcgetattr(fd)
##    try:
##        tty.setraw(sys.stdin.fileno())
##        ch = sys.stdin.read(1)
## 
##    finally:
##        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
##    return ch
## 
##button_delay = 0.2

def heardEnter():
    global character
    i,o,e = select.select([sys.stdin],[],[], 0)
    for s in i:
        if s == sys.stdin:
            character = sys.stdin.read(1)
            return True
    return False

def main():
    global character, player, input_state1, input_state2, last_state1
    global last_state2, video, video1, video2, quit_video, killPause, kill, killPrime
    millis = lambda: int(round(time.time() * 1000))
    lastRed = millis()
    lastGreen = millis()
    while True:
        kill = GPIO.input(26)
        ##quit_video = GPIO.input(21)
        

        if kill == True and (millis() - lastRed > 500):
            killPause = not killPause
            lastRed = millis()
            print(killPause)
            
        if not killPause:
            img.close()
            if heardEnter():
                os.system('killall omxplayer.bin')
                player = False
                if character == '0':
                    if player:
                        os.system('killall omxplayer.bin')
                        player = False
                    player = True
                    omxc = Popen(['omxplayer', '-b', video2])
                    omxc.wait()
                    player = False
                    
                elif character == '1':
                    if player:
                        os.system('killall omxplayer.bin')
                        player = False
                    
                    omxc = Popen(['omxplayer', '-b', '--loop', '--no-osd', video])
                    player = True
                elif character == '2':
                    if player:
                        os.system('killall omxplayer.bin')
                        player = False
                    
                    omxc = Popen(['omxplayer', '-b', '--loop', '--no-osd', video1])
                    player = True
                elif character == 27:
                    exit(0)
            
            else:
                input_state1 = GPIO.input(16)
                if input_state1 == True and (millis() - lastGreen > 500):
                    print(input_state1)
                    if (player):
                        os.system('killall omxplayer.bin')
                        omxc = Popen(['omxplayer', '-b', '--loop', '--no-osd', video1])
                        player = True
                    else:
                        omxc = Popen(['omxplayer', '-b', '--loop', '--no-osd', video1])
                        player = True
                    lastGreen = millis()
                else:
                    if (not player):
                        omxc = Popen(['omxplayer', '-b', '--loop', '--no-osd', video])
                        player = True

                last_state1 = input_state1
        else:
            if player:
                os.system('killall omxplayer.bin')
                player = False
            img.show()
                
if __name__ == '__main__':
    main()
