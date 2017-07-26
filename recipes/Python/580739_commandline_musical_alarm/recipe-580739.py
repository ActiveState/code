from __future__ import print_function

'''
musical_alarm_clock.py

Author: Vasudev Ram
Copyright 2016 Vasudev Ram
Web site: https://vasudevram.github.io
Blog: http://jugad2.blogspot.com
Product store: https://gumroad.com/vasudevram

Description: A simple program to make the computer act like 
a musical alarm clock. Start it running from the command line 
with a command line argument specifying the number of minutes 
after which to give the alarm. It will wait for that long, and 
then play a musical sound a few times.
'''

import sys
import string
from playsound import playsound, PlaysoundException
from time import sleep, asctime

sa = sys.argv
lsa = len(sys.argv)
if lsa != 2:
    print("Usage: python {} duration_in_minutes.".format(sys.argv[0]))
    print("Example: python {} 10".format(sys.argv[0]))
    print("Use a value of 0 minutes for testing the alarm immediately.")
    print("The program plays a musical sound a few times after the duration is over.")
    sys.exit(1)

try:
    minutes = int(sa[1])
except ValueError:
    print("Invalid value {} for minutes.".format(sa[1]))
    print("Should be an integer >= 0.")
    sys.exit(1)

if minutes < 0:
    print("Invalid value {} for minutes.".format(minutes))
    print("Should be an integer >= 0.")
    sys.exit(1)

seconds = minutes * 60

if minutes == 1:
    unit_word = "minute"
else:
    unit_word = "minutes"

try:
    print("Current time is {}.".format(asctime()))
    if minutes > 0:
        print("Alarm set for {} {} later.".format(str(minutes), unit_word))
        sleep(seconds)
    else:
        print("Running in immediate test mode, with no delay.")
    print("Alarm time reached at {}.".format(asctime()))
    print("Wake up.")
    for i in range(5):
        playsound(r'c:\windows\media\chimes.wav')        
        #sleep(1.00)
        sleep(0.50)
        #sleep(0.25)
        #sleep(0.10)
except PlaysoundException as pe:
    print("Error: PlaysoundException: message: {}".format(pe))
    sys.exit(1)
except KeyboardInterrupt:
    print("Interrupted by user.")
    sys.exit(1)
