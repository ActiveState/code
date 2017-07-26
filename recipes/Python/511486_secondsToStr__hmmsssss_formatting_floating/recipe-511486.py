def secondsToStr(t):
    rediv = lambda ll,b : list(divmod(ll[0],b)) + ll[1:]
    return "%d:%02d:%02d.%03d" % tuple(reduce(rediv,[[t*1000,],1000,60,60]))



# example usage

import time

t1 = time.time()
# perform long-running task
t2 = time.time()

print "Elapsed time:", secondsToStr( t2-t1 )
