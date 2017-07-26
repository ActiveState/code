"""
symbols.py -- by bearophile, V.1.0 Jan 23 2007

This module is probably an useless toy to manage symbols with CPython.

The symbol 'car' can be defined with as  Symbol('s_car')  or they are
  automatically instantiated inside functions/methods with the help
  of the  @withsymbols  decorator.

Some ideas come from Pythologic.py by Shai Berger, Cookbook recipe n.303057
"""

class Symbol:
    """Symbol class. A symbol 'car' has to be defined as:
      Symbol('inprefixcar')
    Where inprefix is a class attribute that's usually s_
    Or you can use the @withsymbols decorator."""
    inprefix = "s_"
    outprefix = "$"
    def __init__(self, inname):
        inname = str(inname)
        if not inname or not inname.startswith(Symbol.inprefix):
            raise TypeError("Symbol names must be defined with a starting "
                            + Symbol.inprefix)
        self.__name = Symbol.outprefix + inname[len(Symbol.inprefix):]
        self.__hash = hash(self.__name)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__name == other.__name

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            raise True
        return self.__name != other.__name

    def __cmp__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Symbols can be compared only with other Symbols")
        return cmp(self.__name, other.__name)

    def __hash__(self):
        return self.__hash

    def __nonzero__(self):
        return True

    def __repr__(self): # this may become __str__
        return self.__name

    def getrepr(self): # this may become __repr__
        return "%s('%s%s')" % (self.__class__.__name__, Symbol.inprefix,
                               self.__name[len(Symbol.outprefix):])
    repr = property(getrepr)


def withsymbols(func):
    """decorator, if applied to a function, allows it to use Symbols,
    creating them when needed when the function is defined. A symbol
    name must start with inprefix (usually s_)."""
    # Ideas derived from Pythologic.py  by Shai Berger
    # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/303057
    try:
        code = func.func_code
    except:
        raise TypeError, "function or method argument expected"
    names = code.co_names
    locally_defined = code.co_varnames
    globally_defined = func.func_globals
    defined = set(locally_defined).union(globally_defined)
    undefined = set(names) - defined

    # Update the global scope of the function func, add definitions
    # for all undefined names starting with inprefix
    for name in undefined:
        if name.startswith(Symbol.inprefix):
            func.func_globals[name] = Symbol(name)
    return func


if __name__ == '__main__':
    @withsymbols
    def symbols_demo():
        print "Symbols demo:"
        print "  {s_a:5, s_b:6, s_c:s_a}:", {s_a:5, s_b:6, s_c:s_a}
        print "  Symbol('s_bar'):", Symbol('s_bar')
        some_symbols = set([(s_a, s_b), s_c, s_d])
        print "  some_symbols:", some_symbols
        print "  s_car == s_car:", s_car == s_car
        print "  s_car is s_car:", s_car is s_car
        print "  s_car, repr(s_car), s_car.repr:", s_car, repr(s_car), s_car.repr
        print "  s_b > s_a, s_b >= s_c:", s_b > s_a, s_b >= s_c
        print '  "|" + str(s_car) + "|":', "|" + str(s_car) + "|"
        print "  sorted([s_d, s_a, s_c, s_f, s_e]):", sorted([s_d, s_a, s_c, s_f, s_e])
        s_hello = 5 # s_name names can be defined anyway in the normal way
        print "  s_hello:", s_hello


    symbols_demo()
