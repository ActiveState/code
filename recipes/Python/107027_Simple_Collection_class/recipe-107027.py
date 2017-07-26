#!/usr/bin/env python

import UserList

class Collection(UserList.UserList):
    """Collections group objects together and forward attribute lookups.

    At least this is the Collection I remember from LYMB (an interpreted OO
    language developed by Bill Lorensen et al at GE CRD), which almost
    certainly got it from Smalltalk.
    """

    def get(self, attr):
        """return a list of attributes from ourselves.

        note that an object in the collection is not required to have 'attr',
        so the result may be shorter than the collection itself."""
        return Collection([getattr(x, attr) for x in self if hasattr(x, attr)])

    def call(self, attr, *args, **kwds):
        """return the result of calling 'attr' for each of our elements"""
        attrs = self.get(attr)
        return Collection([x(*args, **kwds)
                             for x in attrs
                               if callable(x)])

if __name__ == "__main__":
    import time

    class Food:
        def __init__(self):
            self.t = time.time()
            time.sleep(0.5)

    class Ham(Food):
        def say(self):
            print "I am Ham, and I don't want any arguments, thank you."
            return ()

        def speak_up(self, arg):
            print 'I am Ham, and my arguments are %s' % arg
            return arg

    class Eggs(Food):
        def speak_up(self, arg='bacon'):
            print 'I am Eggs, and my arguments are %s' % arg
            return arg

    class Spam(Food):
        def shout(self, arg1, arg2='sausage'):
            print 'I AM SPAM AND MY ARGUMENTS ARE %s AND %s' % (arg1, arg2)
            return (arg1, arg2)

    c = Collection()
    # kind of boring example...
    c.extend(range(3))
    print c.get("__hash__")
    print c.call("__hash__")
    print

    # slightly more interesting example...
    c = Collection([Ham(), Eggs(), Spam()])

    print "*** when was this food made? ***"
    times = c.get("t")
    print map(round, times, [2]*len(times))
    print

    print "*** what kind of food is it? ***"
    print c.get("__class__").get("__name__")
    print

    print "*** shouting ***"
    print c.call("shout", "nickel", "dime")
    print

    print "*** speaking up ***"
    print c.call("speak_up", "juice please")
    print

    print "*** saying ***"
    print c.call("say")
    print
