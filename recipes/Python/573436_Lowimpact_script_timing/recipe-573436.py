# timing.py
#   by Paul McGuire, May, 2008
#
import atexit
import time

__all__ = ""

def secondsToStr(t):
    rediv = lambda ll,b : list(divmod(ll[0],b)) + ll[1:]
    return "%d:%02d:%02d.%03d" % \
                tuple(reduce(rediv,[[t*1000,],1000,60,60]))

def printTimeMarker(s,printElapsed=False):
    def printCurrentTime():
        print
        print "="*40
        print s
        print "%d/%02d/%02d %02d:%02d:%02d" % time.localtime()[:6]
        if printElapsed:
            print "Elapsed time:", secondsToStr(time.time() - startTime)
        print "="*40
        print
    return printCurrentTime
    
atexit.register(printTimeMarker("Program end",True))

printTimeMarker("Program start")()
startTime = time.time()
