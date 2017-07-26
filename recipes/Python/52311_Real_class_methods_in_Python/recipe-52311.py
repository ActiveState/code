class _ClassMethod:
    # Helper class: instances represent methods bound to a class
    def __init__(self, klass, func):
        self.func = func
        # oops: circular reference!
        self.klass = klass

    def __call__(self, *args, **kw):
        # return result of function call
        return self.func(self.klass, *args, **kw)

import ExtensionClass

class Class(ExtensionClass.Base):
    def __class_init__(self):
        # automagically convert methods to class methods
        #
        # ExtensionClass.Base calls this _class_ method after the _class_
        # has been created!
        for mth in self.__class_methods__:
            self.__dict__[mth.func_name] = _ClassMethod(self, mth)
        
    def class_method(self, *args, **kw):
        # A _class method_ creating an returning new a new instance
        # the 'self' argument is actual class itself
        print "class_method called with", self, args, kw
        return self()

    def class_method_2(self, *args, **kw):
        # Class methods may return anything they like
        print "class_method_2 called with", self, args, kw
        return None

    def instance_method(self, *args, **kw):
        # instance methods behave normally
        print "instance_method called with", self, args, kw

    # List the methods which should be automagically be converted
    # into class methods
    __class_methods__ = class_method, class_method_2

class Subclass(Class):
    def class_method_2(self):
        # override a class method in a subclass
        print "Hi from", self


####################################################################

c = Class()

# demonstrate calling class methods
print Class.class_method()
print Class.class_method(1, 2, 3, a=10, b=20, c=30)
print Subclass.class_method()
print Class.class_method_2()
print Subclass.class_method_2()

# demonstrate calling instance methods
c.instance_method()
try:
    Class.instance_method()
except Exception, detail:
    print "Called instance method off the class:\n\t", detail

# calling class methods off an instance also works...
print c.class_method()
