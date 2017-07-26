#!/usr/bin/env python
# specialrange.py
"""
Contains a general purpose object for arbitrary ranges

i.e.
a-z = abcdefghijklmnopqrstuvwxyz
A-Z = ABCDEFGHIJKLMNOPQRSTUVWXYZ
1-9 = 123456789
0-9 = 0123456789
0-1000 = 0123456789...1000

Copyright 2011 by Sunjay Varma. All Rights Reserved.
Check out www.sunjay.ca
"""

LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE = LOWERCASE.upper()
LETTERS = LOWERCASE+UPPERCASE
NUMBERS = "123456789"

try:
    basestring
    xrange

except NameError:
    basestring = str
    xrange = range

class irange(object):

    def __init__(self, start, stop=None, step=1):
        if stop is None:
            stop = start
            start = 0
                    
        if not isinstance(start, (float, int)) and not isinstance(stop, (float, int)) and \
           type(start) != type(stop):
            raise TypeError("The types of start and stop must be the same!")

        try:
            if "." in start:
                start = float(start)
            else:
                start = int(start)
            if "." in stop:
                stop = float(stop)
            else:
                stop = int(stop)
        except (ValueError, TypeError):
            pass # will be handled later
        
        if isinstance(start, basestring): # the types of start and stop will be the same
            assert len(start) and len(stop), "There must be at least one character!"
            
            if len(start) > 1 or len(stop) > 1:
                raise ValueError("Longer start and stop values are unsupported!")
            if start in LETTERS and stop in LETTERS:
                self.iterrange = self._char_range(start, stop, step)
            else:
                self._cannot_understand(start, stop, step)

        elif isinstance(start, (float, int)):
            self.iterrange = self._number_range(start, stop, step)
        else:
            self._cannot_understand(start, stop, step)
            
    def _cannot_understand(self, start, stop, step):
        raise ValueError("Cannot understand: %s, %s, or %s"%(start, stop, step))

    @staticmethod
    def _in_seq(seq, *args):
        for x in args:
            if x not in seq:
                return False
        return True
    
    def _char_range(self, start, stop, step):
        is_lower = self._in_seq(LOWERCASE, start, stop)
        if not(is_lower or self._in_seq(UPPERCASE, start, stop)):
            raise ValueError("start and stop must both be in the uppercase or lowercase letters")
        seq = is_lower and LOWERCASE or UPPERCASE
        start_i = seq.index(start)
        stop_i = seq.index(stop)
        delta = abs((start_i - stop_i) // step) #+ 1 # the +1 will give even the last character in the result

        if stop_i < start_i and step >= 0 or stop_i > start_i and step <= 0:
            # the number will never reach
            return iter([])
        return (seq[start_i + step * i] for i in xrange(delta))
        
    @staticmethod
    def _number_range(start, stop, step):
        if stop < start and step >= 0 or stop > start and step <= 0:
            # the number will never reach
            return iter([])
        delta = abs((start - stop) // step)
        return (start + step * i for i in xrange(int(delta)))

    def __iter__(self):
        return self

    def next(self):
        return self.iterrange.next()

    def __next__(self): # py3
        return self.iterrange.__next__()

srange = lambda start, stop=None, step=1: list(irange(start, stop, step))
