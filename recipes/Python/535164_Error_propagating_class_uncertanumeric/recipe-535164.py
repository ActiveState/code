#!/usr/bin/python
# -*- coding: utf8 -*-
# Uncertain quantities.
# (c) Robert Jordens <jordens@debian.org>
# Made available freely under the Python license

import numpy as np
from enthought.traits.api import HasStrictTraits
from enthought.traits.api import Str, Float, Bool, List, Dict, Enum

class Uncertain(HasStrictTraits):
    """
    Represents a numeric value with a known small uncertainty 
    (error, standard deviation...).
    Numeric operators are overloaded to work with other Uncertain or
    numeric objects.
    The uncertainty (error) must be small. Otherwise the linearization
    employed here becomes wrong.
    The usage of traits can easily be dumped.
    """
    value = Float
    error = Float(0.)
    def __init__(self, value=0., error=0., *a, **t):
        self.value = value
        self.error = abs(error)
        super(Uncertain, self).__init__(*a, **t)
    def __str__(self):
        return "%g+-%g" % (self.value, self.error)
    def __repr__(self):
        return "Uncertain(%s, %s)" % (self.value, self.error)
    def __float__(self):
        return self.value
    def assign(self, other):
        if isinstance(other, Uncertain):
            self.value = other.value
            self.error = other.error
        else:
            self.value = other
            self.error = 0.
    def __abs__(self):
        return Uncertain(abs(self.value), self.error)
    def __add__(self, other):
        if isinstance(other, Uncertain):
            v = self.value + other.value
            e = (self.error**2+other.error**2)**.5
            return Uncertain(v, e)
        else:
            return Uncertain(self.value+other, self.error)
    def __radd__(self, other):
        return self + other # __add__
    def __sub__(self, other):
        return self + (-other) # other.__neg__ and __add__
    def __rsub__(self, other):
        return -self + other # __neg__ and __add__
    def __mul__(self, other):
        if isinstance(other, Uncertain):
            v = self.value * other.value
            e = ((self.error*other.value)**2+(other.error*self.value)**2)**.5
            return Uncertain(v, e)
        else:
            return Uncertain(self.value*other,
                    self.error*other)
    def __rmul__(self, other):
        return self * other # __mul__
    def __neg__(self):
        return self*-1 # __mul__
    def __pos__(self):
        return self
    def __div__(self, other):
        return self*(1./other) # other.__div__ and __mul__
    def __rdiv__(self, other):
        return (self/other)**-1. # __pow__ and __div__
    def __pow__(self, other):
        if isinstance(other, Uncertain):
            v = self.value**other.value
            e = ((self.error*other.value*self.value**(other.value-1.))**2+
                (other.error*np.log(self.value)*self.value**other.value)**2)**.5
            return Uncertain(v, e)
        else:
            return Uncertain(self.value**other,
                    self.error*other*self.value**(other-1))
    def __rpow__(self, other):
        assert not isinstance(other, Uncertain)
            # otherwise other.__pow__ would have been called
        return Uncertain(other**self.value,
                self.error*np.log(other)*other**self.value)
    def exp(self):
        return np.e**self
    def log(self):
        return Uncertain(np.log(self.value), self.error/self.value)
