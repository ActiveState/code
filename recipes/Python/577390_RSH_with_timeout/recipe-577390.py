#!/usr/bin/python

import subprocess
import time
import sys
import os
from optparse import OptionParser

rsh = "/usr/bin/rsh"
    
def rshTimed(host, command, timeOut):
  rshD = subprocess.Popen([rsh,host,command],stdout=sys.stdout,stderr=sys.stdout)
  timeStart = time.time()
  if(timeOut != 0):
    while(1):
      # Check if timeOut secs have passed since the execution of rsh
      if(int(time.time() - timeStart) > int(timeOut)):
	# Kill the process if timed out
	rshD.kill()
	break
      # Check if the execution of rsh is done before the timeOut value
      elif(rshD.poll() == 0):
	break
      # Sleep for a sec before the next loop.
      time.sleep(1)
  try:
    # If rsh is killed then reap it 
    eStatus = os.waitpid(rshD.pid, 0)[1]
  except:
    # If rsh has been completed successfully 
    eStatus = rshD.returncode
  return(eStatus)
     
  
    
if(__name__ == "__main__"):
  usage = "%prog [-t TIMEOUT] hostname command"
  optParser = OptionParser(usage)
  optParser.add_option("-t","--timeOut",dest="timeOut",help="Timeout value for rsh in seconds",default=0,metavar="TIMEOUT")
  (options, args) = optParser.parse_args()
  if(len(args) < 2):
    optParser.error("incorrect number of arguments")
    sys.exit(1)
  eStatus = rshTimed(args[0],args[1],options.timeOut)
  print("\n")
  sys.exit(eStatus)
