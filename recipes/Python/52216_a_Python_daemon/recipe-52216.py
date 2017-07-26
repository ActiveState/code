import sys 
import os  
if os.fork()==0:
    os.setsid()
    sys.stdout=open("/dev/null", 'w')
    sys.stdin=open("/dev/null", 'r')
    while(1):
        # Daemon's main code goes here                 
        pass

sys.exit(0)
