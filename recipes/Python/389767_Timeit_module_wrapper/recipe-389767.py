#!/usr/bin/python
# A simple wrapper for the timeit module.
import timeit

def Timeit(func,number=10000,module="__main__"):
    """ A wrapper which can
    be used to time any function """

    name = func.__name__
    t = timeit.Timer("%s()"%name, "from %s import %s" % (module, name))
    return "%.2f usec/pass" % (1000000*t.timeit(number=number)/number)

if __name__=="__main__":
    from mymodule import test
    
    # Using wrapper
    print Timeit(test)
    # Directly using timeit
    t = timeit.Timer("test()", "from __main__ import test")
    print "%.2f usec/pass" % (1000000*t.timeit(number=10000)/10000)    
