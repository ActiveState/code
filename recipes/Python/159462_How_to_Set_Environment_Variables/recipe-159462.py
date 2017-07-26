setvar.bat
----------
@echo off
python setvarp.py %1 %2 %3 %4 %5 %6 %7 %8 %9
settmp
del settmp.bat

setvarp.py
----------
import sys, time, math
key = sys.argv[1]
value = eval(' '.join(sys.argv[2:]))
command = 'set %s=%s\n' % (key, value)
open('settmp.bat', 'w').write(command)


sample command line session
---------------------------
C>setvar ts time.ctime()
C>setvar pi 22.0 / 7.0
C>setvar pyver sys.version
C>set

TS=Sun Oct 27 18:12:23 2002
PI=3.14285714286
PYVER=2.3a0 (#29, Oct 22 2002, 01:41:41) [MSC 32 bit (Intel)]
