#!/usr/bin/env /usr/local/bin/python
import time
TIME=str(time.time())
LEFT=TIME[3:9]
RIGHT=TIME[10:13]
print ("\nstatic char *CVSid%s%s=\"@(#) $Header$ \";\n" % (LEFT,RIGHT))
