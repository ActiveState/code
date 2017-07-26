"""
  This module is helpful when something must be done on a timer.
  It is for testing purposes but the main class can be used in other applications
  with modifications to the timerExpired function. You can put your own stuff in there
  that must happen when the timer has expired.
  
  It is used by executing it from the shell with arguments -t, -s and optional -x.
  argument -t: timer duration in seconds.
  argument -s: choice to stop the timer after a default 5 seconds,
  optional -x: if -s was 'y' and an delay in seconds before the timer must be stopped.
  
  
  Author: Johan Geldenhuys
          AccessTel
  Date  : 2005-08-11
  
"""

# The threading module is used that has the code to start
# and stop the timer instance, so, why not use it?
from threading import Timer

# time module is imported to sleep a while after timer is started 
# before stopping it.
import time

# Main class to get timer instance going
class timer:
      
      # start timer with n seconds and go to self.timerExpired
      def startTimer(self, n):
        self.t = Timer(n, self.timerExpired)
        print 'Timer started for %d seconds'% n
        
        #start the timer instance
        self.t.start()
        
      # Called if argument is true to stop it.
      def stopTimer(self):
        
        # First look if the timer is active
        if self.t.isAlive():
                print 'Timer found active'
                
                #Stop the timer instance
                self.t.cancel()
                print 'Timer stopped'
        
        # If not active, do nothing
        else:
                print 'Timer inactive'
                
      # Put code in here to execute after timer has expired.
      def timerExpired(self):
        print 'Timer expired, go to do what you want'
        
# Help the user understand how to use this module
def printUsageAndExit():
    print
    print "Usage: %s -t[time-out] "\
          "-s[sleep before stopping, 'y' or 'n'] \r\noptional -x[seconds to wait before stopping]\r\n\r\n"\
          "Example: timertest.py -t 10 -s y -x 6\r\n" % sys.argv[0]
    print
    sys.exit(1)

    
if __name__ == '__main__':
        
        import sys, getopt, string
        
        l = (len(sys.argv))
        
        if l <= 4:
           printUsageAndExit()
        arg3 = int('5')
        optlist, args = getopt.getopt(sys.argv[1:], "t:s:x:")
        for opt in optlist:
            
            if opt[0] == '-t':
               if not (opt[1].isdigit()):
                  printUsageAndExit()
               arg1 = int(opt[1])
               
            elif opt[0] == '-s':
               arg2 = (opt[1])
                  
               #printUsageAndExit()
               
               
            elif opt[0] == '-x':
               if not (opt[1].isdigit()):
                  printUsageAndExit()
               arg3 = int(opt[1])
               
        
        x = timer()
        if arg2 == 'y':
           x.startTimer(arg1)
           time.sleep(arg3)
           print 'You chose to stop the timer after %s with option %s'%(str(arg3), arg2)
           x.stopTimer()
           
        if arg2 == 'n':
           x.startTimer(arg1)
           
