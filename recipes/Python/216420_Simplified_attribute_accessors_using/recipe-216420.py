#!/usr/bin/env python

__version__ = "1.0"

"""OverloadedAccessors.py

This recipe presents an ideom for simplified accessors, that combines
typical getter and setter functionality of an attribute into a single
overloaded method, that instead of getATTRIBUTE and setATTRIBUTE can
now just be called ATTRIBUTE. When called without arguments it acts as
a getter and retrieves the attribute's value. When called with
arguments, the attribute is set to this value.

Keywords: accessor, getter, setter, overload, read/only attribute,
          unique value, default argument
"""

omitted=[]                   # omitted contains an exclusive unique value


class Person:
    def __init__(self, givenName, name):
        self._givenName=givenName
        self._name=name

    # read write accessor
    def givenName(self, value=omitted):
        if value is not omitted: # check for exclusive unique value
            self._givenName=value
        return self._givenName

    # read only accessor
    def name(self):
        return self._name


print ("The special unique value has the id %s. No other Python object is "
       "identical (unsing the 'is' operator) to it.\n" % id(omitted))
    
            
p=Person('Ulrich', 'Hoffmann')

print p.givenName(), p.name()      # Read attributes through accessors

print p.givenName('Ulrich Ernst')  # Write attribute through accessor

print p.givenName(), p.name()

try:
    print p.name("")                   # Read/only accessor
except TypeError:
    print "I cannot set the value of 'name' in object %s. This is expected." % p
