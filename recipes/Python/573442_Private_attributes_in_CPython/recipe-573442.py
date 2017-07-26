# privates.py

import sys
import itertools

class PrivateAccessError(Exception):
    pass

class PrivateDataMetaclass(type):
    def __new__(metacls,name,bases,dct):

        function = type(lambda x:x)

        privates = set(dct.get('__private__',()))

        codes = set()
        for val in dct.itervalues():
            if isinstance(val,function):
                codes.add(val.func_code)

        getframe = sys._getframe
        count = itertools.count

        def __getattribute__(self,attr):
            if attr in privates:
                for i in count(1):
                    code = getframe(i).f_code
                    if code in codes:
                        break
                    if code.co_name != '__getattribute__':
                        raise PrivateAccessError(
                            "attribute '%s' is private" % attr)
            return super(cls,self).__getattribute__(attr)

        def __setattr__(self,attr,val):
            if attr in privates:
                for i in count(1):
                    code = getframe(i).f_code
                    if code in codes:
                        break
                    if code.co_name != '__setattr__':
                        raise PrivateAccessError(
                            "attribute '%s' is private" % attr)
            return super(cls,self).__setattr__(attr,val)

        dct['__getattribute__'] = __getattribute__
        dct['__setattr__'] = __setattr__

        cls = type.__new__(metacls,name,bases,dct)

        return cls


# And now for a few tests

import traceback

class A(object):
    __metaclass__ = PrivateDataMetaclass
    __private__ = ['internal']

    def __init__(self,n):
        self.internal = n

    def inc(self):
        self.internal += 1

    def res(self):
        return self.internal

class B(A):
    __private__ = ['internal2']

    def __init__(self,n,m):
        super(B,self).__init__(n)
        self.internal2 = m

    def inc(self):
        super(B,self).inc()
        self.internal2 += 2

    def res(self):
        return self.internal2 + super(B,self).res()

    def bad(self):
        return self.internal2 + self.internal

a = A(1)
a.inc()

print "Should print 2:"
print a.res()
print

print "Should raise PrivateAccessError:"
try:
    print a.internal
except PrivateAccessError:
    traceback.print_exc()
print

b = B(1,1)
b.inc()

print "Should print 5:"
print b.res()
print

print "Should raise PrivateAccessError:"
try:
    print b.internal2
except PrivateAccessError:
    traceback.print_exc()
print

print "Should raise PrivateAccessError:"
try:
    print b.bad()
except PrivateAccessError:
    traceback.print_exc()
print
