class Base(object):
   def __init__(self, *args, **kwds):
       self.autosetup(self.__class__, [], **kwds)

   def setup(self, **kwds):
       pass

   def autosetup(self, cls, called, **kwds):
       for base in cls.__bases__:
           try:
               b = base.setup
           except AttributeError:
               pass
           else:
               if b not in called:
                   called = self.autosetup(base, called, **kwds)

       cls.setup(self, **kwds)
       called.append(cls.setup)
       return called

# Sample Usage
class A(Base):
   def setup(self, foo, **kwds):
       print "A",foo

class B(Base):
   def setup(self, blah, **kwds):
       print "B", blah

class C(B):
   def setup(self, blech, **kwds):
       print "C", blech

class D(A, C):
   def setup(self, frog, **kwds):
       print "D", frog

class E(C):
   pass

class F(D, E):
   def setup(self, toad, foo, frog, **kwds):
       print "F", foo, frog, toad

x = F(foo=1, blah=2, blech=3, frog=4, toad=5)
