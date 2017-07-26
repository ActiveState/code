#!/usr/bin/env python
"""
Emulates a pomodoro timer.

The program is invoked with a "work duration" and a "rest duration".
It plays a ticking sound for the work duration (specified in minutes) and then an alarm.
After that it plays another tick for the rest duration (also specified in minutes).

If the PyOSD library is available, it will use it to display messages
on the screen. Otherwise, it simply prints them out to stdout.

This is usually invoked as
./ticker.py 30 5
This means that you work for 30 minutes and then rest for 5.

For details on the Pomodoro technique, please refer http://www.pomodorotechnique.com/
For the sound files, please check out http://www.soundjay.com/clock-sounds-1.html

This script is an attempt to create an offline version of http://www.focusboosterapp.com/live.cfm

"""

import sys
import time
import subprocess

pyosd = False
try:
    import pyosd
    osd = pyosd.osd()
    osd.set_align(pyosd.ALIGN_CENTER)
    osd.set_pos(pyosd.POS_MID)
    display = osd.display
except:
    display = lambda x: sys.stdout.write(str(x)+"\n")
    
WORK_TICK = "/home/noufal/scratch/clock-ticking-4.mp3"
REST_TICK = "/home/noufal/scratch/clock-ticking-5.mp3"
ALARM     = "/home/noufal/scratch/alarm-clock-1.mp3"
DEV_NULL  = open("/dev/null","w")

def tick(duration, tick):
    "Plays a the ticking sound specified by tick for duration time"
    cmd = ["mpg123", "--loop", "-1" , tick]
    p = subprocess.Popen(cmd, stdout = DEV_NULL, stderr = subprocess.PIPE)
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        display("Interrupting")
    p.kill()
    
def alarm(alarm):
    "Plays the alarm sound specified by alarm"
    cmd = ["mpg123", alarm]
    p = subprocess.Popen(cmd, stdout = DEV_NULL, stderr = subprocess.PIPE)
    p.wait()
    
def main(args):
    if len(args[1:]) != 2:
        print "Usage : %s work_time rest_time"%args[0]
        return -1
    twork, trest = args[1:]
    display("Work now")
    tick(int(twork)*60, WORK_TICK)
    alarm(ALARM)
    display("Rest now")
    tick(int(trest)*60, REST_TICK)
    alarm(ALARM)
    display("Cycle complete")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
