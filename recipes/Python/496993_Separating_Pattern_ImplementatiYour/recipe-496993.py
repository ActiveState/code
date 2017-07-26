##########
# pattern_impl.py
##########
from installmethod import installmethod # the installmethod from recipe: 223613

class ObserverPattern:
    """
    A reusable implementation of the Observer pattern.
    """
    theSubject = None
    observers = {}
    
    class Subject:
        def __init__(self):
            self.observers = []
        
        def attach(self, observer):
            self.observers.append(observer)
        
        def detach(self, observer):
            self.observers.remove(observer)
        
        def notify(self):
            for observer in self.observers:
                observer.update(self)
        
        def decoration(self):
            self.decorated_trigger()
            self.notify()
    
    class Observer:
        def __init__(self, subject):
            subject.attach(self)
        
        def update(self, observer):
            currentState = observer.get_current_state()
            self.react_to_observation(currentState)
    
    def specify_subject(self, subject):
        self.theSubject = subject
        self.make_generalization(subject, self.Subject)
    
    def add_observer(self, observer):
        self.observers[observer.__name__] = observer
        self.make_generalization(observer, self.Observer)
    
    def make_generalization(self, childClass, parentClass):
        bases = list(childClass.__bases__)
        bases.append(parentClass)
        childClass.__bases__ = tuple(bases)
    
    def make_observation(self, changeObservation, changeReaction):
        func = getattr(self.theSubject, changeObservation)
        installmethod(func, self.theSubject, "get_current_state")
        
        for observer in self.observers.keys():
            func = getattr(self.observers[observer], changeReaction)
            installmethod(func, self.observers[observer], "react_to_observation")
    
    def add_trigger(self, trigger):
        func = getattr(self.theSubject, trigger)
        installmethod(func, self.theSubject, "decorated_trigger")
        
        func = getattr(self.theSubject, "decoration")
        installmethod(func, self.theSubject, trigger)

##########
# example.py
##########
class ClockTimer:
    def get_time(self):
        # get current state of the subject
        return self.currentTime
    
    def tick(self):
        # update internal time-keeping state
        import time
        self.currentTime = time.ctime()

class DigitalClock:
    def draw(self, currentTime):
        # display currentTime as a digital clock
        print "DigitalClock: current time is", currentTime

class AnalogClock:
    def draw(self, currentTime):
        # display currentTime as an analog clock
        print "AnalogClock: current time is", currentTime

if __name__ == '__main__':
    from pattern_impl import ObserverPattern
    
    observerPattern = ObserverPattern()
    
    observerPattern.specify_subject(ClockTimer)
    
    observerPattern.add_observer(DigitalClock)
    observerPattern.add_observer(AnalogClock)
    
    observerPattern.make_observation("get_time", "draw")
    observerPattern.add_trigger("tick")
    
    aTimer = ClockTimer()
    dClock = DigitalClock(aTimer)
    aClock = AnalogClock(aTimer)
    
    import time
    for i in range(10):
        print "\nTick!"
        aTimer.tick()
        time.sleep(1)
