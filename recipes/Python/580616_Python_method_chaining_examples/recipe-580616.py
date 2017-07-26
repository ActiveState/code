'''
Program: string_processor.py
Demo of method chaining in Python.
By: Vasudev Ram - 
http://jugad2.blogspot.in/p/about-vasudev-ram.html
Copyright 2016 Vasudev Ram
'''

import copy

class StringProcessor(object):
    '''
    A class to process strings in various ways.
    '''
    def __init__(self, st):
        '''Pass a string for st'''
        self._st = st

    def lowercase(self):
        '''Make lowercase'''
        self._st = self._st.lower()
        return self

    def uppercase(self):
        '''Make uppercase'''
        self._st = self._st.upper()
        return self

    def capitalize(self):
        '''Make first char capital (if letter); make other letters lower'''
        self._st = self._st.capitalize()
        return self

    def delspace(self):
        '''Delete spaces'''
        self._st = self._st.replace(' ', '')
        return self

    def rep(self):
        '''Like Python's repr'''
        return self._st

    def dup(self):
        '''Duplicate the object'''
        return copy.deepcopy(self)

def process_string(s):
    print
    sp = StringProcessor(s)
    print 'Original:', sp.rep()
    print 'After uppercase:', sp.dup().uppercase().rep()
    print 'After lowercase:', sp.dup().lowercase().rep()
    print 'After uppercase then capitalize:', sp.dup().uppercase().\
    capitalize().rep()
    print 'After delspace:', sp.dup().delspace().rep()

def main():
    print "Demo of method chaining in Python:"
    # Use extra spaces between words to show effect of delspace.
    process_string('hOWz  It     GoInG?')
    process_string('The      QUIck   brOWn         fOx')

main()
