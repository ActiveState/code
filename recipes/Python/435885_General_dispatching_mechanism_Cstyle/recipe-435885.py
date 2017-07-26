# dispatch.py

# definitions:

import threading

class Dispatcher(object):
    def __init__(self, targets=None, nonBlocking=True):
        if not targets or targets is None:
            self._targets = []
        else:
            self._targets = targets
        self._nonBlocking = nonBlocking
    def __iadd__(self, target):
        self._targets.append(target)
        return self
    def __isub__(self, target):
        self._targets.remove(target)
        return self
    def isNonBlocking(self):
        return self._nonBlocking
    nonBlocking = property(isNonBlocking)
    def __call__(self, *listArgs, **kwArgs):
        def invokeTargets():
            for target in self._targets:
                target(*listArgs, **kwArgs)
        if self.nonBlocking:
            threading.Timer(0, invokeTargets).start()
        else:
            invokeTargets()

# demos:

def Test1():
    """
    A simple example demonstrating most functionality.
    """
    def m1():
        print 'm1 invoked'
    def m2():
        print 'm2 invoked'
    e = Dispatcher()
    e += m1
    e += m2
    e += m2
    print 'Dispatching:'
    e()
    e -= m1
    print 'Dispatching:'
    e()
    e -= m2
    print 'Dispatching:'
    e()

def Test2():
    """
    A more realistic example for the OO programmer.
    """
    class Sprite(object):
        def __init__(self, location):
            self._location = location
        locationChanged = Dispatcher()
        def getLocation(self):
            return self._location
        def setLocation(self, newLocation):
            oldLocation = self._location
            self._location = newLocation
            # Dispatch a "property change event"
            self.locationChanged(oldLocation, newLocation)
        location = property(getLocation, setLocation)
    s = Sprite((2,4))
    def SpriteLocationChanged(oldLocation, newLocation):
        print 'oldLocation =', oldLocation
        print 'newLocation =', newLocation
    s.locationChanged += SpriteLocationChanged
    s.location = (3,4)
    s.location = (4,4)

if __name__ == '__main__':
    Test1()
    Test2()
