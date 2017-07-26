from threading import *
from mx.DateTime import *

class myThread(Thread):
    def __init__(self, target, args=(), name=None):
        # we need a tuple here
        if type(args)<>type((1,)):
            args = (args,)
        Thread.__init__(self, target=target, name=name, args=args)
        self._uptime = now()
        self.start()

    def getUptime(self):
        return self._uptime

    def __str__(self):
        return self.getName()

def GetThreads():
    " doesn't list mainthread "
    return filter(lambda x: x.getName()<>"MainThread", enumerate())

if __name__=="__main__":
    import time
    def DoSome(s=""):
        print "now it's ", now()
        for i in range(3):
            print s, now()
            time.sleep(1)

    t1 = myThread(DoSome, ("one"))
    t2 = myThread(DoSome, ("two"))

    time.sleep(0.5)
    for t in GetThreads(): 
        print t, t.getUptime()
