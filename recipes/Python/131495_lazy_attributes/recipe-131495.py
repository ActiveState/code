#
# first solution:
#

class sample(object):
    class one(object):
        def __get__(self, obj, type=None):
            print "computing ..."
            obj.one = 1
            return 1
    one = one()

x=sample()
print x.one
print x.one


#
# other solution:
#  

# lazy attribute descriptor
class lazyattr(object):
    def __init__(self, fget, doc=''):
        self.fget = fget
        self.__doc__ = doc
    def __appoint__(self, name, cl_name):
        if hasattr(self,"name"):
            raise SyntaxError, "conflict between "+name+" and "+self.name
        self.name = name        
    def __get__(self, obj, cl=None):
        if obj is None:
            return self
        value = self.fget(obj)
        setattr(obj, self.name, value)
        return value

# appointer metaclass:
# call the members __appoint__ method 
class appointer(type):
    def __init__(self, cl_name, bases, namespace):
        for name,obj in namespace.iteritems():
            try:
                obj.__appoint__(name, cl_name)
            except AttributeError:
                pass
        super(appointer, self).__init__(cl_name, bases, namespace)

# base class for lazyattr users
class lazyuser(object):
    __metaclass__ = appointer

# usage sample
class sample(lazyuser):
    def one(self):
        print "computing ..."
        return 1
    one  = lazyattr(one, "one lazyattr")

x=sample()
print x.one
print x.one
del x.one
print x.one
