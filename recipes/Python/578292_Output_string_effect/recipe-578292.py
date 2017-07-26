#!/usr/bin/python3

import sys
import time

string = input('Any string you want: ')
s = 0
while s < len(string):
    sys.stdout.write(string[s])
    sys.stdout.flush()
    time.sleep(0.06) # set the time milliseconds for faster output
    s = s + 1
sys.stdout.write('\n')
