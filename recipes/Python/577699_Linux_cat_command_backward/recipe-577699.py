#!/usr/bin/python
import sys
import os.path
import os

if len(sys.argv) < 2:
    print('Usage: %s file_name' % sys.argv[0])

fp = open(sys.argv[1],'r')
#size = os.path.getsize(sys.argv[1]) 
fp.seek(-1, 2)  

try:
    data = ''
    data = fp.read(1)
    while True:
        fp.seek(-2, 1)
        t = fp.read(1)
        if t == '\n':
            print data
            data = ''
        else:
            data = t+data
except Exception, e:
    print data
    sys.exit(0)

print data
