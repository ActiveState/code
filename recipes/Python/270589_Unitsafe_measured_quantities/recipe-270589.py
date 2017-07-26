def demo():
    # The definition of measure classes is straightforward, for example:
    class Length(object):
        __metaclass__ = MeasureType
        DEFAULT_UNIT = "m"
        _TO_DEFAULT = { "mm":0.001, "cm":0.01, "km":1000,
                        "in":0.0254, "ft":0.3048, "yd":0.9144, "mi":1609.34
                      }
    
    l1 = Length(12.3,'cm')
    l2 = Length(50,'mm')
    Length.setDefaultUnit("in")
    print l1+l2             # "6.811024 in"
    print 3*l2.value("m")   # "0.15"
    print l1>l2             # "True"

    # Measures with arbitrary unit conversion functions, like temperature,
    # are also supported:
    class Temperature(object):
        __metaclass__ = MeasureType
        DEFAULT_UNIT = "Celsius"
        _TO_DEFAULT =   { "Fahrenheit" : lambda tf: 5.0/9.0 * (tf-32) }
        _FROM_DEFAULT = { "Fahrenheit" : lambda tc: 9.0/5.0 * tc + 32 }

#todo:
# - support for unit prefixes (e.g. "c" for 10^-2, "k" for 10^3", etc.);
#   thus "cm", "km", etc. won't have to be specified for Length
# - unit name aliases (e.g. "kilometers","km")
# - compound measures: 
#   a. Compound measure definition (e.g. Velocity)
#   b. Modify *,/ to be allowed between any Measure instances (e.g. Length/Duration)
#   c. Combine a and b (?)
# - thorough unit testing

__author__ = "George Sakkis"

class MeasureType(type):
    '''Metaclass for supporting unit-safe measure objects. Classes generated with 
      this as metaclass (e.g. Length, Area, Temperature, etc.) must define the 
      following class-scope variables:
      1.  DEFAULT_UNIT (a string), and 
      2a. either _TO_DEFAULT, a dictionary that maps each other unit to
          - either a constant number, which is interpreted as the ratio of the
            unit to the DEFAULT_UNIT
          - or a function, for more complicate conversions from the unit to
            DEFAULT_UNIT (e.g. from Celsius to Fahrenheit).
       2b. or _FROM_DEFAULT. Inverse of _TO_DEFAULT, maps each unit
            (other than the DEFAULT_UNIT) to the function that
            returns the measure in this unit, given the DEFAULT_UNIT
            (e.g. from Fahrenheit to Celsius).
      If there is at least one function present, both _TO_DEFAULT and _FROM_DEFAULT
      have to be given (so that both the function and its inverse are defined).'''
    
    def __new__(cls,classname,bases,classdict):
        defUnit = classdict["DEFAULT_UNIT"]
        toDefault = classdict.get("_TO_DEFAULT") or {}
        fromDefault = classdict.get("_FROM_DEFAULT") or {}
        units = uniq([defUnit] + toDefault.keys() + fromDefault.keys())
        restUnits = units[1:]
        # form convertion matrix
        conversion_matrix = {}
        # 1. non-default unit -> default unit
        for unit in restUnits:
            try: conversion_matrix[(unit,defUnit)] = toDefault[unit]
            except KeyError:
                try: conversion_matrix[(unit,defUnit)] = 1.0 / fromDefault[unit]
                except (KeyError,TypeError): raise LookupError, "Cannot convert %s to %s" % (unit,defUnit)
        # 2. default unit -> non-default unit
        for unit in restUnits:
            # check if toDefault[unit] is number
            try: conversion_matrix[(defUnit,unit)] = fromDefault[unit]
            except KeyError:
                try: conversion_matrix[(defUnit,unit)] = 1.0 / toDefault[unit]
                except (KeyError,TypeError): raise LookupError, "Cannot convert %s to %s" % (defUnit,unit)
        # 3. non-default unit -> non-default unit
        for fromUnit in restUnits:
            for toUnit in restUnits:
                if fromUnit != toUnit:
                    try: conversion_matrix[(fromUnit,toUnit)] = conversion_matrix[(fromUnit,defUnit)] \
                                                               * conversion_matrix[(defUnit,toUnit)]
                    except TypeError: 
                        conversion_matrix[(fromUnit,toUnit)] = \
                                lambda value: conversion_matrix[(defUnit,toUnit)](
                                                conversion_matrix[(fromUnit,defUnit)](value))
        ## print conversion_matrix
        # 4. convert all constants c to functions lambda x: c*x
        for (k,v) in conversion_matrix.iteritems():
            try: conversion_matrix[k] = lambda x,i=float(v): x*i
            except (TypeError,ValueError): pass
        # update classdict                                        
        assert "_CONVERT_UNITS" not in classdict
        classdict["_CONVERT_UNITS"] = conversion_matrix
        classdict["_UNITS"] = units
        if "_TO_DEFAULT" in classdict: del classdict["_TO_DEFAULT"]
        if "_FROM_DEFAULT" in classdict: del classdict["_FROM_DEFAULT"]
        # set Measure to be base a class of cls
        bases = tuple(uniq((MeasureType.Measure,) + bases))
        return type.__new__(cls,classname,bases,classdict)

    class Measure(object):
        '''The superclass of every Measure class. Concrete measure classes
           don't have to specify explicitly this class as their superclass; 
           it is added implicitly by the MeasureType metaclass.'''
        
        __slots__  = "_value", "_unit"
        
        def setDefaultUnit(cls,unit):
            if unit != cls.DEFAULT_UNIT:
                cls.__verifyUnit(unit)
                cls.DEFAULT_UNIT = unit
        setDefaultUnit = classmethod(setDefaultUnit)

        def value(self, unit=None):
            if unit == None: unit = self.__class__.DEFAULT_UNIT
            self.__verifyUnit(unit)
            return self.__convert(self._value, self._unit, unit)

        def __init__(self, value, unit=None):
            if unit == None: unit = self.__class__.DEFAULT_UNIT
            self.__verifyUnit(unit)
            self._unit = self.__class__.DEFAULT_UNIT
            self._value = self.__convert(value, unit, self._unit)
                        
        def __str__(self,unit=None):
            if unit == None: unit = self.__class__.DEFAULT_UNIT
            return "%f %s" % (self.value(unit), unit)
        
        def __abs__(self): return self.__class__(abs(self._value), self._unit)
        
        def __neg__(self): return self.__class__(-self._value, self._unit)
    
        def __cmp__(self,other):
            try: return cmp(self._value, self.__coerce(other))
            except ValueError: return cmp(id(self),id(other))

        def __add__(self,other):
            try: return self.__class__(self._value + self.__coerce(other), self._unit)
            except ValueError: raise ValueError, "can only add '%s' (not '%s') to '%s'" \
                                                % (self.__class__.__name__,
                                                   other.__class__.__name__,
                                                   self.__class__.__name__)
        def __sub__(self,other):
            try: return self.__class__(self._value - self.__coerce(other), self._unit)
            except ValueError: raise ValueError, "can only subtract '%s' (not '%s') from '%s'" \
                                                % (self.__class__.__name__,
                                                   other.__class__.__name__,
                                                   self.__class__.__name__)
        def __iadd__(self,other):
            try: self._value += self.__coerce(other)
            except ValueError: raise ValueError, "can only increment '%s' (not '%s') by '%s'" \
                                                % (self.__class__.__name__,
                                                   other.__class__.__name__,
                                                   self.__class__.__name__)
    
        def __isub__(self,other):
            try: self._value -= self.__coerce(other)
            except ValueError: raise ValueError, "can only decrement '%s' (not '%s') by '%s'" \
                                                % (self.__class__.__name__,
                                                   other.__class__.__name__,
                                                   self.__class__.__name__)
    
        def __mul__(self,other):
            try: return self.__class__(self._value * float(other), self._unit)
            except TypeError: raise ValueError, "can only multiply '%s' (not '%s') by a number" \
                                                % (self.__class__.__name__, other.__class__.__name__)
            
        __rmul__ = __mul__        
                        
        def __div__(self,other):
            try: return self.__class__(self._value / float(other), self._unit)
            except TypeError: raise ValueError, "can only divide '%s' (not '%s') by a number" \
                                                % (self.__class__.__name__, other.__class__.__name__)
        def __imul__(self,other):
            try: self._value *= float(other)
            except TypeError: raise ValueError, "can only multiply '%s' (not '%s') by a number" \
                                                % (self.__class__.__name__, other.__class__.__name__)
    
        def __idiv__(self,other):
            try: self._value /= float(other)
            except TypeError: raise ValueError, "can only divide '%s' (not '%s') by a number" \
                                                % (self.__class__.__name__, other.__class__.__name__)
        
        def __pow__(self,other):
            try: return self.__class__(self._value ** float(other), self._unit)
            except TypeError: raise ValueError, "can only raise '%s' to a number (not '%s')" \
                                                % (self.__class__.__name__, other.__class__.__name__)
            
        def __ipow__(self,other):
            try: self._value **= float(other)
            except TypeError: raise ValueError, "can only raise '%s' to a number (not '%s')" \
                                                % (self.__class__.__name__, other.__class__.__name__)
            
        ################################## 'private' Methods ##################################
    
        def __convert(cls, value, fromUnit, toUnit):
            if fromUnit == toUnit: return value
            else: return cls._CONVERT_UNITS[(fromUnit,toUnit)](value)
        __convert = classmethod(__convert)
        
        def __verifyUnit(cls,unit):
            if unit not in cls._UNITS:
                raise ValueError, "'%s' is not a recognized %s unit (pick one from %s)" % \
                                  (unit, cls.__name__, ', '.join(["'%s'" % u for u in cls._UNITS]))
        __verifyUnit = classmethod(__verifyUnit)
        
        def __coerce(self,other):
            if type(self) != type(other) or not isinstance(self,MeasureType.Measure):
                raise ValueError
            return self.__convert(other._value,other._unit,self._unit)


def uniq(sequence):
    '''Removes the duplicates from the given sequence, preserving the order
       of the remaining elements.'''
    dict = {}
    try:
        return [dict.setdefault(i,i) for i in sequence if i not in dict]
    except TypeError:   # unhashable item(s)
        return [dict.setdefault(repr(i),i) for i in sequence if repr(i) not in dict]

if __name__ == '__main__': demo()
