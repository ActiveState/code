import weakref
import exceptions
import threading   # for lock

class RecursionError(exceptions.RuntimeError):
    pass

class _subscription(object):
    """A subscription is returned as a result of subscribing to an 
       observable. When the subscription object is finalized, the 
       subscription is cancelled.  This class is used to facilitate 
       subscription cancellation."""

    def __init__(self, subscriber, observed):
        self.subscriber = subscriber
        self.observed = weakref.ref(observed)

    def __del__(self):
        obsrvd = self.observed()
        if (self.subscriber and obsrvd):
            obsrvd._cancel(self.subscriber)


class _obwan(object):
    '''Half-hidden class.  Only 'observable should construct these.
    Calls to subscribe, cancel get invoked through the observable.
    _obwan objects reside in class instances containing observables.'''

    def __init__(self):
        self.subscribers = []
        self._value = None
        self._changeLock = threading.Lock()
        
    def __call__(self):
        """returns the current value, the one last set"""
        return self._value

    def _notifySubscribers(self, value):
        for (f,exceptionHdlr) in self._callbacks():
            try:
                f(value)
            except Exception, ex:
                if exceptionHdlr and not exceptionHdlr(ex): 
                    raise            # reraise if not handled

    def setvalu(self, value):
        """Notify the subcribers only when the value changes."""
        if self._value != value:
            if self._changeLock.acquire(0):     # non-blocking
                self._value = value
                try:
                    self._notifySubscribers(value)
                finally:
                    self._changeLock.release()
            else:
                raise RecursionError("Attempted recursion into observable's set method.")

    def subscribe(self, obsv, exceptionInfo = None):
        observer = obsv.setvalu if isinstance(obsv, _obwan) else obsv
        ob_info =(observer, exceptionInfo)
        self.subscribers.append(ob_info)
        return _subscription(ob_info, self)

    def _callbacks(self):
       scribers = []
       scribers.extend(self.subscribers)
       return scribers

    def _cancel(self, wref):
        self.subscribers.remove(wref)


class Observable(object):
    """An observable implemented as a descriptor. Subscribe to an observable 
    via calling  xxx.observable.subscribe(callback)"""
    def __init__(self, nam):
        self.xname = "__"+nam
        self.obwan = _obwan

    def __set__(self,inst, value ):
        """set gets the instances associated variable and calls 
        its setvalu method, which notifies subribers"""
        if inst and not hasattr(inst, self.xname):
            setattr(inst, self.xname, self.obwan())
        ow = getattr(inst, self.xname)
        ow.setvalu(value)

    def __get__(self, inst, klass):
        """get gets the instances associated variable returns it"""
        if inst and not hasattr(inst, self.xname):
            setattr(inst, self.xname, self.obwan())
        return getattr(inst, self.xname)

#-----------------------------------------------------------------------
#   Example & Simple Test
#-----------------------------------------------------------------------
if __name__ == '__main__':

    class MyClass(object):
        """ A Class containing the observables length and width"""
        length = Observable('length')
        width = Observable('width')

        def __init__(self):
            self.length.setvalu(0)
            self.width.setvalu(0)
            

    class MyObserver(object):
        """An observer class. The initializer is passed an instance
           of 'myClass' and subscribes to length and width changes.
           This observer also itself contains an observable, l2"""
        
        l2 = Observable('l2')

        def __init__(self, name, observedObj):
            self.name = name
            self.subs1 = observedObj.length.subscribe(self.print_l)
            self.subs2 = observedObj.width.subscribe(self.print_w)
            
            """An observable can subscribe to an observable, in which case
              a change will chain through both subscription lists.
              Here l2's subscribers will be notified whenever observedObj.length
              changes"""
            self.subs3 = observedObj.length.subscribe(self.l2)

        def print_w(self, value):
            print "%s Observed Width"%self.name, value

        def print_l(self, value):
            print "%s Observed Length"%self.name, value
            
        def cancel(self):
            """Cancels the instances current subscriptions. Setting self.subs1 to
            None removes the reference to the subscription object, causing it's 
            finalizer (__del__) method to be called."""
            self.subs1 = None
            self.subs2 = None
            self.subs3 = None

    def pl2(value):
        print "PL2 reports ", value
        if type(value) == type(3):
            raise ValueError("pl2 doesn't want ints.")

    def handlePl2Exceptions( ex ):
        print 'Handling pl2 exception:', ex, type(ex)
        return True     # true if handled, false if not
            
    area = MyClass()
    kent = MyObserver("Kent", area)
    billy = MyObserver("Billy", area)
    subscription = billy.l2.subscribe(pl2, handlePl2Exceptions)

    area.length = 6
    area.width = 4
    area.length = "Reddish"

    billy.subs1 = None
    print "Billy shouldn't report a length change to 5.15."
    area.length = 5.15      
    billy.cancel()
    print "Billy should no longer report"
    area.length = 7
    area.width = 3
    print "Areas values are ", area.length(), area.width()

    print "Deleting an object with observables having subscribers is ok"
    area = None
    area = MyClass()
    print "replaced area - no subscribers to this new instance"
    area.length = 5
    area.width ="Bluish"
    c = raw_input("ok? ")
