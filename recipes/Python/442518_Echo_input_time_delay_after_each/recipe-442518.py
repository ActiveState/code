"""dribble.py: Echo input with a time delay after each line

Usage: dribble.py [-time] [files...]

    'time' is the delay after lines in seconds, with a default of 1 second.
    'files...' is a list of files to echo.  If no files a specified,
               echo the standard input.
               
Examples:

        dribble.py -2 test1.txt test2.txt
    
    Echo the files 'test1.txt' and 'test2.txt' with a delay of 2 seconds
    between each line.
    
        ls -l | dribble.py -0.5
        
    Echo the directory listing produced by 'ls -l' with a delay of 1/2 seconds.
"""

import sys
import fileinput
import time

if len(sys.argv)>1:
    if sys.argv[1] in ('-h', '--help', '/?'):
        print __doc__
        sys.exit(0)
        
    delay_time = 1.0  # Seconds
    if sys.argv[1][0] == '-' and len(sys.argv[1])>1:
        delay_time = float(sys.argv[1][1:])
        sys.argv.pop(1)
    
for line in fileinput.input():
    print line,
    time.sleep(delay_time)
    
