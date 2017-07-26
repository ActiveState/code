import weakref
import sys
import threading   # for lock

class RecursionError(RuntimeError):
    pass

class _subscription:
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


class _observed:
    '''Half-hidden class.  Only 'observable' should construct these.
    Calls to subscribe, cancel get invoked through the observable.
    observed objects reside in class instances containing observables.'''

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
            except Exception as ex:
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
        observer = obsv.setvalu if isinstance(obsv, _observed) else obsv
        ob_info =(observer, exceptionInfo)
        self.subscribers.append(ob_info)
        return _subscription(ob_info, self)

    def _callbacks(self):
       scribers = []
       scribers.extend(self.subscribers)
       return scribers

    def _cancel(self, wref):
        self.subscribers.remove(wref)


class Observable:
    """An observable implemented as a descriptor. Subscribe to an observable 
    via calling  xxx.observable.subscribe(callback)"""
    def __init__(self, nam):
        self.xname = "__"+nam
        self.observed = _observed

    def __set__(self,inst, value ):
        """set gets the instances associated variable and calls 
        its setvalu method, which notifies subribers"""
        if inst and not hasattr(inst, self.xname):
            setattr(inst, self.xname, self.observed())
        ow = getattr(inst, self.xname)
        ow.setvalu(value)

    def __get__(self, inst, klass):
        """get gets the instances associated variable returns it"""
        if inst and not hasattr(inst, self.xname):
            setattr(inst, self.xname, self.observed())
        return getattr(inst, self.xname)

#-----------------------------------------------------------------------
#   Example & Simple Test
#-----------------------------------------------------------------------
if __name__ == '__main__':
    import unittest
    
    class MyClass:
        """ A Class containing the observables length and width"""
        length = Observable('length')   #argument string should match the
                                        #variable name
        width = Observable('width')

        def __init__(self):
            self.length.setvalu(0)
            self.width.setvalu(0)
            

    class MyObserver:
        """An observer class. The initializer is passed an instance
           of 'myClass' and subscribes to length and width changes.
           This observer also itself contains an observable, l2"""
        
        l2 = Observable('l2')

        def __init__(self, name, observedObj):
            self.name = name
            self.subscrptn1 = observedObj.length.subscribe(self.print_length)
            self.subscrptn2 = observedObj.width.subscribe(self.print_width)
            
            """An observable can subscribe to an observable, in which case
              a change will chain through both subscription lists.
              Here l2's subscribers will be notified whenever observedObj.length
              changes"""
            self.subscrptn3 = observedObj.length.subscribe(self.l2)
            self.w = self.l = None

        def print_width(self, value):
            print ("%s Observed Width"%self.name, value)
            self.w = value

        def print_length(self, value):
            print ("%s Observed Length"%self.name, value)
            self.l = value
            
        def cancel(self):
            """Cancels the instances current subscriptions. Setting self.subscrptn1
            to None removes the reference to the subscription object, causing it's 
            finalizer (__del__) method to be called."""
            self.subscrptn1 = None
            self.subscrptn2 = None
            self.subscrptn3 = None

    def PrintLen2(value):
        print ("PrintLen2 reports ", value)
        if type(value) == type(3):
            raise ValueError("PrintLen2 doesn't want ints.")

    def handlePl2Exceptions( ex ):
        print ('Handling pl2 exception:', ex, type(ex))
        return ( type(ex)== ValueError )
       

    class ObserverTestCases(unittest.TestCase):
      area = MyClass()
      kent = MyObserver("Kent", area)
      billy = MyObserver("Billy", area)

      # here we set up a chained observer. PrintLen2 function is called when
      # billy.l2 changes. handlePl2Exceptions is exception handler for PrintLen2.
      # if PrintLen2 throws an Exception, handlePl2Exceptions will be called to
      # handle them.
    
      subscription = billy.l2.subscribe(PrintLen2, handlePl2Exceptions)

      def test_01(self):
        self.area.length = 6
        self.assertEqual(self.kent.l, 6)
        self.assertEqual(self.billy.l, 6)
        
        self.area.width = 4
        self.assertEqual(self.kent.w, 4)
        self.assertEqual(self.billy.w, 4)
        
        self.area.length = "Reddish"
        self.assertEqual(self.kent.l, "Reddish")
        self.assertEqual(self.billy.l, "Reddish")

      def test_02(self):
        self.billy.subscrptn1 = None
        print ("Billy shouldn't report a length change to 5.15.")
        self.area.length = 5.15
        self.assertEqual(self.kent.l, 5.15)
        self.assertEqual(self.billy.l, "Reddish")
        
      def test_03(self):
        self.billy.cancel()
        print ("Billy should no longer report")
        self.area.length = 7
        self.assertEqual(self.kent.l, 7)
        self.assertEqual(self.billy.l, "Reddish")
        self.area.width = 3
        self.assertEqual(self.kent.w, 3)
        self.assertEqual(self.billy.w, 4) # existing value

        self.assertEqual(self.area.length(), 7)
        self.assertEqual(self.area.width(), 3)

      def test_04(self):
        print ("Deleting an object with observables having subscribers is ok")
        self.area = None
        self.area = MyClass()
        print ("replaced area - no subscribers to this new instance")
        self.area.length = 5
        self.assertEqual(self.kent.l,7)
        self.assertEqual(self.billy.l, "Reddish")
        self.area.width ="Bluish"
        self.assertEqual(self.kent.w, 3)
        self.assertEqual(self.billy.w, 4)


    c = input("ok? ")
    unittest.main()
