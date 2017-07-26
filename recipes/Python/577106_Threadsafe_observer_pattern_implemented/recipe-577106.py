from Observer import _obwan, Observable
import threading
from synchlock import synchronous

class _tsobwan(_obwan):
    """Subclassed _obwan to provide thread synchronization"""

    def __init__(self):
        _obwan.__init__(self)
        self._synchLock = threading.RLock()

    setvalu = synchronous('_synchLock')(_obwan.setvalu)
    subscribe = synchronous('_synchLock')(_obwan.subscribe)
    _callbacks = synchronous('_synchLock')(_obwan._callbacks)
    _cancel = synchronous('_synchLock')(_obwan._cancel)

class TSObservable(Observable):
    """Subclassed to provide thread synchronization"""
    
    def __init__(self, nam ):
        self.xname = "__"+nam
        self.obwan = _tsobwan

# -------------------------------------------------------------------------
# example case

if __name__ == "__main__":

    class MyClass(object):
        """ A Class containing the observables chancellor and width"""
        chancellor = TSObservable('chancellor')
        width = TSObservable('width')

        def __init__(self):
            self.chancellor.setvalu(0)
            self.width.setvalu(0)


    class MyObserver(object):
        """Provides Observers for above"""

        def __init__(self, name, observedObj):
            self.name = name
            self.subs1 = observedObj.chancellor.subscribe(self.print_c)
            self.subs2 = observedObj.width.subscribe(self.print_w)
            self.timesToReport = len(name)

        def print_c(self, value):
            print "%s observed change "%self.name, value
            self.timesToReport -= 1
            if self.timesToReport == 0:
                print "  cancelling my subscription"
                self.subs1 = None

        def print_w(self, value):
            print "%s observed value "%self.name, value

    
    def report2(value):
        print "Report 2 observed value of ",value

    import threading
    import time
    def onRun(observed, name):
        obsver = MyObserver(name, observed)
        isrunning = True
        for j in range(400):
            time.sleep(.10)
            if isrunning and obsver.timesToReport==0:
                isrunning = False
                observed.chancellor = obsver.name

    # ----------------------------------------------------
    obnames = """Bob AllisonJane Karl Mujiburami Becky Geraldine
       Johnny Barbarah Matthew""".split()

    area = MyClass()
    rptsbscrbr = area.width.subscribe(report2)

    thrds = [ threading.Thread(target=onRun, name=n, args=(area,n))
                for n in obnames]

    for thrd in thrds:
        thrd.start()

    # lots of reports on changes to width
    area.width = 4
    area.width = "reddish"
    # lots of reports on changes to chancellor
    area.chancellor = 1.5
    area.chancellor = 9
    print " "
    time.sleep(4.0)
    # Resursing starts as thread cancel subscriptions
    area.chancellor = "Amy" 
    # wait awhile...
    time.sleep(4)
    area.width =7.1

    c = raw_input("ok?")
      
