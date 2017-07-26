import time

class GovernedRange(object):
    def __init__(self, low, high, speed=1):
        """
        Returns a range of floats, where each consecutive number is 
        incremented at a speed * time between iterations, rather than 
        a set value.
        low: start of range
        high: top of range
        speed: amount to increment, per second.
        """
        self.speed = float(speed)
        self.low = float(low)
        self.high = float(high)
        self._i = self.low
        self._t = time.time()
    
    def __iter__(self):
        while True:
            yield self.next()
            
    def next(self):
        speed = float(self.speed)
        inc = speed * (time.time() - self._t)
        i = self._i
        i += inc
        self._t = time.time()
        if i >= self.high: raise StopIteration
        self._i = i
        return i
        

for x in GovernedRange(1,5,speed=1):
    print x
    time.sleep(0.1)
    
