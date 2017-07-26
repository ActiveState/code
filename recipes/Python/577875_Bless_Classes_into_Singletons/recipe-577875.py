def AreYouSingle(func):
    """ Test function for verifying singularity """
    
    s1 = func()
    s2 = func()
    return (s1==s2)

class SingletonBlesserMeta(type):
    """ Type for Singleton Blesser class """

    @staticmethod
    def klsnew(cls, *args):
        if not cls.instance:
            cls.instance = object.__new__(cls)
        return cls.instance

    def my_new(cls,name,bases=(),dct={}):        
        return None

    @classmethod
    def bless(cls, *args):
        for klass in args:
            klass.instance = None
            if object in klass.__bases__:
                klass.__new__ = classmethod(cls.klsnew)

    def __init__(cls, name, bases, dct={}, *args):
        super(SingletonBlesserMeta, cls).__init__(name, bases, dct)
        cls.instance = None
        cls.__new__ = cls.my_new
        
class SingletonBless(object):
    """ Bless classes into Singletons """
    __metaclass__ = SingletonBlesserMeta

class A(object): pass
class B(object): pass
class C: pass

if __name__ == "__main__":
    # Bless the classes to make them singletons
    SingletonBless.bless(A, B, C)
    print AreYouSingle(A)
    print AreYouSingle(B)
    # Will work only if class is derived from "object"
    # so this prints False
    print AreYouSingle(C)    
