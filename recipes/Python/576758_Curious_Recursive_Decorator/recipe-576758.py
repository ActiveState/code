import abc

def keycomparable(Derived):
    class KeyComparableImpl(metaclass = abc.ABCMeta):
        @abc.abstractmethod
        def _cmpkey(self):
            pass

        def __lt__(self, other):
            if not isinstance(other, Derived):
                return NotImplemented
            return self._cmpkey() < other._cmpkey()
        
        def __le__(self, other):
            if not isinstance(other, Derived):
                return NotImplemented
            return self._cmpkey() <= other._cmpkey()

        def __eq__(self, other):
            if not isinstance(other, Derived):
                return NotImplemented
            return self._cmpkey() == other._cmpkey()
        
    
    class Wrapper(Derived, KeyComparableImpl):
        pass

    Wrapper.__name__ = Derived.__name__
    Wrapper.__doc__ = Derived.__doc__        
    return Wrapper


@keycomparable
class IntABS:
    "sample class"
    def __init__(self,val):
        self.val = val

    def _cmpkey(self):
        return abs(self.val)

    def __str__(self):
        return str(abs(self.val))

    def __repr__(self):
        return "abs({0})".format(self.val)
