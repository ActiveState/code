#!/usr/bin/env python

class Super:
    def methodA(self):
        print 'Super class methodA.'

class Delegated:
    def methodA(self):
        print 'Delegated class methodA.'

    def methodB(self):
        print 'Delegated class methodB.'

class X (Super):
    def __init__(self, delegate=None):
        self.delegate = delegate
    def __getattr__(self, name):

        return getattr(self.delegate, name)

delegated = Delegated()
x = X(delegated)
x.methodA()
x.methodB()


# Running this code.
# >> $ python delgate.py 
# >> Super class methodA.
# >> Delegated class methodB.
