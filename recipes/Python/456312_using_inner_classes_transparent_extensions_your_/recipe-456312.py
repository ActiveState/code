class Property(object):
    _obj = []
    class __metaclass__(type):
        def __get__(cls, obj, objtype=None):
            if obj is not None:
                cls._obj.append( obj )
            return cls

    @staticmethod
    def parent_instancemethod(func):
        """
            decorator makes the decorated Property method behave like 
            the Property's parent's instance method
        """
        @classmethod
        def _parent_instancemethod(cls, *args, **kwds):
            return func(cls._obj.pop(), *args, **kwds)
        return _parent_instancemethod
    

    @staticmethod
    def parent_classmethod(func):
        """ 
            decorator makes the decorated Property method behave like 
            the Property's parent's class method
        """
        @classmethod
        def _parent_classmethod(cls, *args, **kwds):
            return func(cls._obj.pop().__class__, *args, **kwds)
        return _parent_classmethod

# Testing
if __name__ == "__main__":
    class A:
        a = 10
    
        def method1(self, *args, **kwds):
            print "-------------------------"
            print "In A.method1()"
            print "    Object: ", self
            print "    Arguements: ", args, kwds
            print "-------------------------"
    
        @classmethod
        def method2(cls, *args, **kwds):
            print "-------------------------"
            print "In A.method2()"
            print "    Class: ", cls
            print "    Arguements: ", args, kwds
            print "-------------------------"
    
        @staticmethod
        def method3(*args, **kwds):
            print "-------------------------"
            print "In A.method3()"
            print "    Arguements: ", args, kwds
            print "-------------------------"
    
        class B(Property):
            a = 99
            b = 'spam'
    
            @Property.parent_instancemethod
            def method1(self, *args, **kwds): 
                print "-------------------------"
                print "In A.B.method1()", args, kwds
                print "    Object: ", self
                print "    Arguements: ", args, kwds
                print "-------------------------"
    
            @Property.parent_classmethod
            def method2(cls, *args, **kwds): 
                print "-------------------------"
                print "In A.B.method2()"
                print "    Class: ", cls
                print "    Arguements: ", args, kwds
                print "-------------------------"
    
            @classmethod
            def method3(cls, *args, **kwds): 
                print "-------------------------"
                print "In A.B.method3()"
                print "    Class: ", cls
                print "    Arguements: ", args, kwds
                print "-------------------------"
    
            @staticmethod
            def method4(*args, **kwds): 
                print "-------------------------"
                print "In A.B.method4()"
                print "    Arguements: ", args, kwds
                print "-------------------------"

    x = A()
    print "x: ", x
    print "x.a: ", x.a
    print "x.B: ", x.B    

    x.method1(1, 2, 3)
    x.method2(4, 5, 6)
    x.method2(7, 8, 9)

    print
    print "x.B.a: ", x.B.a 
    print "x.B.b: ", x.B.b 

    x.B.method1('A', 'B', 'C')
    x.B.method2('D', 'E', 'F')
    x.B.method3('G', 'H', 'I')
    x.B.method4('J', 'K', 'L')
