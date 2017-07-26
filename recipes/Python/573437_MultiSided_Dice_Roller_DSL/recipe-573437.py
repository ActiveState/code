#!/usr/bin/python
print """
pyRepl to DM Helper
    Invocation:
        python -i d20.py
    Usage:
        <N>*d(<S>)+<M>
        N   Number of dice
        S   Number of sides on die
        M   Modifier on die roll
    Example:
        >>> 3*d(6)+12
        17
        >>> 2*d(6,True)+12 #shows individual rolls
        4
        2
        18
"""

from random import choice

class d(object):
    def __init__(self,sides,show_rolls=False):
        self.show=show_rolls;
        self.sides=sides
    def roll(self):
       return choice(range(1,self.sides+1)) 
    def accum(self,rolls):
        accum=0;
        for roll in range(rolls):
            roll=self.roll()
            if self.show: print roll
            accum+=roll
        return accum
    def __rmul__(self,other):
        try:
            return self.accum(int(other))
        except ValueError:
            print "Only multiply by an INTEGER"
