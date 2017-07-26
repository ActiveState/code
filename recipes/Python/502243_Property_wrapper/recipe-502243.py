def propertx(fct):
    '''
        Decorator to simplify the use of property.
        Like @property for attrs who need more than a getter.
        For getter only property use @property.
    '''
    arg=[None, None, None, None]
    for i, f in enumerate(fct()):
        arg[i] = f
    if not arg[3] :
        arg[3]=fct.__doc__
    return property(*arg)

if __name__=='__main__':

    class example(object):
        def __init__(self):
            self._a=100
        @propertx
        def bar():
            # BAR doc
            def get(self):
                return self._a
            def set(self, val):
                self._a=val
            return get, set

    foo=example()
    print foo.bar
    foo.bar='egg'
    print foo.bar
