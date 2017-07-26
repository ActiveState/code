import atexit

class AutoCloseMeta(type):
   "Tracks the instances and closes them in reverse instantiation order"

   def __new__(mcl, name, bases, dic):
       cls = super(AutoCloseMeta, mcl).__new__(mcl, name, bases, dic)
       cls.closeall # assert the method closeall exists
       cls._open_instances = [] # objects not closed yet
       return cls

   def __call__(cls, *args, **kw):
       # tracks the instances of the instances
       self = super(AutoCloseMeta, cls).__call__(*args, **kw)
       cls._open_instances.append(self)
       return self

   def closeall(cls):
       "Recursively close all instances of cls and its subclasses"
       print 'Closing instances of %s' % cls # you may remove this print
       for obj in reversed(cls._open_instances):
           obj.close()
           cls._open_instances.remove(obj)
       for subc in cls.__subclasses__():
           subc.closeall()

class AutoClose(object):
    "Abstract base class"
    __metaclass__ = AutoCloseMeta

atexit.register(AutoClose.closeall)

if __name__ == '__main__': # test
    import logging

    class C(AutoClose):
       def __init__(self, id):
           self.id = id
       def close(self):
           logging.warn('closing object %s' % self.id)

    class D(C):
       pass

    c1 = C(1)
    c2 = C(2)
    d3 = D(3)
