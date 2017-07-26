# File: mm0.py / mm1.py
#Jerol Harrington, May 10, 2005
# adapted from Fredrik Lundh's Python Standard Library
# This shows how two processes can talk to another using mmap.

import mmap
import os
import time

filename = "sample.txt"

file = open(filename, "r+")
size = os.path.getsize(filename)

data = mmap.mmap(file.fileno(), size)
while True:
    if data[0] == "G":
        print "Process 0 = Go"
        data[1]="S"
    else:
        print "Process 0 = Stop"
        data[1]="G"
    time.sleep(2)

#for the 2nd file, mm1.py, replace the while loop with
#the following:

#while True:
#    if data[1] == "G":
#        print "Process 1 = Go"
#        data[0]="G"
#    else:
#        print "Process 1 = Stop"
#        data[0]="S"
#    time.sleep(2)
