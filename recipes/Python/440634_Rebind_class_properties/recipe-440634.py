########## Solution I (Better) ##########
# Inspired by many other recipes in this cookbook.
class lazyproperty(object):
    def __init__(self, fget=None, fset=None, fdel=None, doc=''):
        for attr in ('fget', 'fset'):
            func = locals()[attr]
            if callable(func):
                setattr(self, attr, func.func_name)
        setattr(self, '__doc__', doc)
                                                                                                                               
    def __get__(self, obj=None, type=None):
        if not obj:
            return 'property'
        if self.fget:
            return getattr(obj, self.fget)()
                                                                                                                               
    def __set__(self, obj, arg):
        if self.fset:
            return getattr(obj, self.fset)(arg)
############ TEST ################
if __name__ == '__main__':
                                                                                                                               
    class A(object):
        def __init__(self):
            self._p = 1
        def _g(self):
            print 'inside A._g'
            return self._p
        def _s(self, p):
            print 'inside A._s'
            self._p = p
        p  = property (_g, _s, None, 'p doc')
        lp = lazyproperty (_g, _s, None, 'p doc')
                                                                                                                               
    class B(A):
        def _g(self):
            print '** inside B._g **'
            return self._p
                                                                                                                               
    b = B()
    print 'property in action'
    print ' ', b.p
    print 'lazyproperty in action'
    print ' ', b.lp
    b.p = 3

########## Solution II (Old one) #########
def rebind(cls):
                                                                                                                               
    props = [attr for attr in dir(cls) if type(getattr(cls, attr)) == property]
                                                                                                                               
    for prop_name in props:
        prop = getattr(cls, prop_name)
        getter_name = setter_name = destroyer_name = 'xxxxxxxx'
        if prop.fget:
            getter_name = prop.fget.__name__
        if prop.fset:
            setter_name = prop.fset.__name__
        if prop.fdel:
            destroyer_name = prop.fdel.__name__
        p_doc = prop.__doc__
        getter = getattr(cls, getter_name, None)
        setter = getattr(cls, setter_name, None)
        destroyer = getattr(cls, destroyer_name, None)
        setattr(cls, prop_name, property(getter, setter, destroyer, p_doc))

############ TEST ################
if __name__ == '__main__':
                                                                                                                                   class A(object):
        def __init__(self):
            self._p = 1
        def _g(self):
            print 'inside A._g'
            return self._p
        def _s(self, p):
            print 'inside A._s'
            self._p = p
        p = property(_g, _s, None, 'p doc')
                                                                                                                                   class B(A):
        def _g(self):
            print '** inside B._g **'
            return self._p
                                                                                                                               
    b = B()
    print b.p
    b.p = 3
                                                                                                                               
    rebind(B)
                                                                                                                               
    b = B()
    print b.p
    b.p = 3
