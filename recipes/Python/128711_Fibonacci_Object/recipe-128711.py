from math import sqrt, pow, floor
from __future__ import generators

class Fibonacci:
    """A simple class which brings functions to calculate Fibonacci numbers
    and make operations between them"""

    def __init__(self):
        self.Phi    = (1 + sqrt(5))/2
        self.PhiP   = (1 - sqrt(5))/2
        self.rs5    = 1/sqrt(5)
        self.succ   = self.unboundedGenerator()

    def __call__(self, n=-1):
        if n == -1:
            return self.next()
        return self.nth(n)

    def next(self):
        """Next Fibonacci number in the sucesion"""
        return self.succ.next()

    def nth(self, n):
        """Calculate the nth Fibonacci Number by formula. Doesn't work for n > 1474"""
        return floor(self.rs5 * (pow(self.Phi, n) - pow(self.PhiP, n)))

    def list(self, k, n):
        """Returns a list from Fibonacci(k) to Fibonacci(n) numbers"""
        return [ self.nth(i) for i in range(k, n + 1) ]

    def first(self, n):
        """Returns a list with the first n Fibonacci numbers"""
        g = self.generator(n)
        return [ g.next() for i in range(n) ]

    def unboundedGenerator(self):
        """Unbounded Fibonacci generator"""
        thisnum, nextnum = 0, 1L
        while 1:
            yield thisnum
            thisnum, nextnum = nextnum, thisnum + nextnum
        return

    def generator(self, n):
        """n-Bounded Fibonacci generator"""
        thisnum, nextnum = 0, 1L
        for i in range(n + 1):
            yield thisnum
            thisnum, nextnum = nextnum, thisnum + nextnum
        return
