#!/usr/bin/env python
#-----------------------------------------------------------------------------
#   Copyright 2003 by Bud P. Bruegger, Sistema, Italy
#   mailto:bud@sistema.it
#   http://www.sistema.it
#-----------------------------------------------------------------------------
#   dynClass -- Dynamic Classes
#   ---------------------------
#   
#   some simple functions for dynamically adding methods, properties
#   and classmethods to classes at runtime.  
#   
#-----------------------------------------------------------------------------

# see http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/81732 
# and http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/81982
# and http://www.python.org/2.2/descrintro.html#property


import new
import sys

def addMethod(classInstance, func, methName=None):
    """adds function as a new method to an existing class
       function should have self as first argument
    """
    meth = new.instancemethod(func, None, classInstance)
    name = methName or func.__name__
    setattr(classInstance, name, meth)
    return name

def addProperty(classInstance, attrName, fget, fset, fdel=None, \
              fdoc="this is magic"):
    """adds a property to an existing class """
    prop = property(fget, fset, fdel, fdoc)
    setattr(classInstance, attrName, prop)

def addClassMethod(classInstance, func, methName=None):
    """adds function as a new class method to an existing class.
       function should have self as first argument
    """
    name = methName or func.__name__
    setattr(classInstance, name, classmethod(func))

def classFromName(className):
    "returns the class instance object"
    return getattr(sys.modules['__main__'], className)

#==========  example usage ====================================================

if __name__ == "__main__":
    pass 

    #-- testing addMethod ------------------

    def func1(self):
        "some test function"
        return "Name is %s" % self._name
    
    def func2(self, comment=''):
        "some test function"
        return "Age is %s %s" % (self._age, comment)
    
    class Example(object):
        "some example class"
    
        def __init__(self, name, age):
            self._name = name
            self._age = age
    
    sarah = Example('Sarah', 5)
    josh = Example('Josh', 2)
    
    addMethod(Example, func1, 'getName')
    addMethod(Example, func2, 'getAge')
    
    lucia = Example('Lucia', 20)
    
    # Does it work as expected?
    
    print sarah.getName()
    print sarah.getAge('at least soon')
    print josh.getName()
    print josh.getAge('and wild')
    print lucia.getName()
    print lucia.getAge('some time ago')
    print "\n-----------------------\n"
    
    
    #-- testing properties ------------------
    
    def getAltName(self):
        return "*" + self._name + "*"
    
    def setAltName(self, val):
        self._name = val[1:-1]
    
    addProperty(Example, 'altName', getAltName, setAltName)
    print sarah.altName
    sarah.altName="*NEW-SARAH*"
    print sarah.altName
    print sarah.getName()
    bud = Example('Bud', 42)
    print bud.altName
    bud.altName="*The king of beers*"
    print bud.altName
    print bud.getName()
    print "\n-----------------------\n"
    
    #-- testing classFromName -----------

    print "The class named 'Example' is %s" % classFromName('Example')
    class EEE(object):
        pass
    print "The class named 'EEE' is %s" % classFromName('EEE')
    print "\n-----------------------\n"

    
    #-- testing addClassMethod -----------------------

    class C(object):
        pass
    def func(cls):
        return "<<%s>>" % cls.__name__

    addClassMethod(C, func, 'className')

    print "the class name is: ", C.className()
