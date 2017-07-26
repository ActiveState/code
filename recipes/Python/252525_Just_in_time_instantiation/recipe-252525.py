class JIT:
    '''
    JIT is a class for Just In Time instantiation of objects.  Init is called
    only when the first attribute is either get or set.
    '''
    def __init__(self, klass, *args, **kw):
        '''
        klass -- Class of objet to be instantiated
        *args -- arguments to be used when instantiating object
        **kw  -- keywords to be used when instantiating object
        '''
        self.__dict__['klass'] = klass
        self.__dict__['args'] = args
        self.__dict__['kw'] = kw
        self.__dict__['obj'] = None

    def initObj(self):
        '''
        Instantiate object if not already done
        '''
        if self.obj is None:
            self.__dict__['obj'] = self.klass(*self.args, **self.kw)

    def __getattr__(self, name):
        self.initObj()
        return getattr(self.obj, name)

    def __setattr__(self, name, value):
        self.initObj()
        setattr(self.obj, name, value)
        
class TestIt:
    def __init__(self, arg, keyword=None):
        print 'In TestIt.__init__() -- arg: %s, keyword=%s' % (arg, keyword)

    def method(self):
        print 'In TestIt.method().'

def oldWay():
    # Create t whether or not it gets used.
    t = TestIt('The Argument', keyword='The Keyword')

def main():
    # JIT refactored
    t = JIT(TestIt, 'The Argument', keyword='The Keyword')
    print 'Not intstaintiated yet.'

    # TestIt object instantiated here.
    t.method()

if __name__ == '__main__':
    main()
    
# OUTPUT:
# Not intstaintiated yet.
# In TestIt.__init__() -- arg: The Argument, keyword=The Keyword
# In TestIt.method().
    
