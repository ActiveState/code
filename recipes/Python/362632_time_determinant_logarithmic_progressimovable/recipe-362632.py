import time
from math import log

class LogarithmicProgression(object):
    """
    A time determinant logarithmic progression, 
    with a movable target and energy factor.
    """
    def __init__(self, position=1, target=1, energy=1):
        self.position = float(position)
        self.target = float(target)
        self.energy = float(energy)
        self.distance = abs(self.target - self.position)
        self._lastCall = time.time()
        
    def next(self):
        if self.target < 0: modTarget = self.target - 1
        else: modTarget = self.target + 1
        self.distance = d = abs(modTarget - self.position)
        if d == 0: return 0.0
        amount = log(d)
        increment = amount * ((time.time() - self._lastCall) * self.energy)
        if self.position < modTarget:
            self.position += increment
        else:
            self.position -= increment
        self._lastCall = time.time()
        return increment
        
if __name__ == "__main__":
    i = LogarithmicProgression(position=0,target=2, energy=1)
    s = time.time()
    for c in xrange(1, 100):
        time.sleep(0.1)
        i.next()
        
    print "0-%.2f in %.2f seconds" % (i.position, time.time() - s)
