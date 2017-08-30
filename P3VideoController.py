import RPi.GPIO as GPIO
import sys, termios, tty, os, time, select
from subprocess import Popen

GPIO.setmode(GPIO.BCM)

GPIO.setup(19, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

video = "Reg.avi"
video1 = "TwoColors.avi"
video2 = "VideoBrief.avi"
last_state1= True
last_state2 = True
input_state1 = True
input_state2 = True
player = False
quit_video = False
character = None

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
    global last_state2, video, video1, video2, quit_video
    
    while True:
        input_state1 = GPIO.input(19)
        quit_video = GPIO.input(21)

        if heardEnter():
            os.system('killall omxplayer.bin')
            player = False
            if character == 'c':
                if player:
                    os.system('killall omxplayer.bin')
                    player = False
                player = True
                omxc = Popen(['omxplayer', '-b', video2])
                omxc.wait()
                player = False
                
            elif character == 'f':
                if player:
                    os.system('killall omxplayer.bin')
                    player = False
                
                omxc = Popen(['omxplayer', '-b', '--loop', '--no-osd', video])
                player = True
            elif character == 27:
                exit(0)
        
        else:
            if (quit_video == True and player):
                os.system('killall omxplayer.bin')
                player = False
            else:
                if (quit_video == False and not player):
                    omxc = Popen(['omxplayer', '-b', '--loop', '--no-osd', video])
                    player = True
            
            if input_state1 != last_state1:
                if (player and not input_state1):
                    os.system('killall omxplayer.bin')
                    omxc = Popen(['omxplayer', '-b', '--loop', '--no-osd', video1])
                    player = True
                elif not input_state1:
                    omxc = Popen(['omxplayer', '-b', '--loop', '--no-osd', video1])
                    player = True

            last_state1 = input_state1

                
if __name__ == '__main__':
    main()
