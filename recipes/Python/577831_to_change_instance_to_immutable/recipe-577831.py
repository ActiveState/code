# -*- coding: utf-8 -*-
"""
immutablize instance sample
"""
import operator
import types



class A(object):
    def __init__(self, a, b):
        self.a = a
        self.__b = b
    
    def say(self):
        print self.a,self.__b
    
    def incr(self):
        self.a = self.a + 100
    
    def incr2(self):
        self.incr()


def frozen_instance(instance):
    def new__(_cls, inst):
        return tuple.__new__(_cls, tuple([inst] + inst.__dict__.values()))
    
    def repr__(self):
        return repr(self[0])
    
    def getattr__(self, name):
        return types.MethodType(self[0].__class__.__dict__[name], self, self[0].__class__)
    klass = instance.__class__
    nlass = type('Frozen'+klass.__name__,(tuple,),
        dict(__new__=new__, __repr__=repr__, __getattr__=getattr__)
    )
    for i,k in enumerate(instance.__dict__.keys()):
        setattr(nlass, k, property(operator.itemgetter(1+i)))
    
    return nlass(instance)




if __name__ == '__main__':
    
    a = A(1, "aaa")
    print "[a]"
    a.say()
    frozen_a = frozen_instance(a)
    print "[frozen_a]"
    frozen_a.say()

    a.incr()
    a.say()
    
    frozen_a.incr2()


-----outputs-----
[a]
1 aaa
[frozen_a]
1 aaa
101 aaa
Traceback (most recent call last):
  File "fix.py", line 58, in <module>
    frozen_a.incr2()
  File "fix.py", line 22, in incr2
    self.incr()
  File "fix.py", line 19, in incr
    self.a = self.a + 100
AttributeError: can't set attribute
