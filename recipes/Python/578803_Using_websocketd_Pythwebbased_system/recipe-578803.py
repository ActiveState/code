An example program that writes to STDOUT:

# psutil_disk_usage.py

import string
from time import sleep
import psutil

print "Disk Space (MB)".rjust(46)
print " ".rjust(25) + "Total".rjust(10) + "Used".rjust(10) + "Free".rjust(10)  
for i in range(5):
    du = psutil.disk_usage('/')
    print str(i + 1).rjust(25) + str(du.total/1024/1024).rjust(10) + str(du.used/1024/1024).rjust(10) + str(du.free/1024/1024).rjust(10)  
    sleep(2)

And a websocketd command that makes the above program into a WebSocket server running on port 8080:

websocketd --port=8080 python psutil_disk_usage.py

You have to give the command:

set PYTHONUNBUFFRED=true

before the above websocketd command is given.
