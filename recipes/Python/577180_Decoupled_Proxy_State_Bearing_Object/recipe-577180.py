#!/usr/bin/env python
import inspect
import multiprocessing
from multiprocessing.managers import SyncManager
import new, sys, types, time, datetime, random

#
#
#
class Commander(object):
   '''
      object to handle all requests
      from delegates. purpose generally to be
      borg or singleton of an object that can
      not be easily shared between different processes.
      Just an Example....
   '''
   def __init__(self, prefix='with_',**kwds):
      self._createTime = datetime.datetime.now()
      self._prefix = prefix
      self.id = random.Random()
      for k,v in kwds.items():
         setattr(self, k, v)
   #
   @property
   def Prefix(self):
      return self._prefix
   #
   @property
   def Commands(self):
      # want a dict comprehension that returns 
      # k,v of name of method, method for
      # method names that start with Prefix
      # but
      # dict comprehensions require another
      # dicussion entirely
      return self.__dict__.items()
   #
   def with_exposed(self, *args, **kwds):
      '''
         method exposed to SyncManager and 'the world'
         will print to std obj ids
      '''
      stack = inspect.stack()[0] # trying to make this file readable
      print '\n***\nCommander_%s.\nwith_exposed(%s, %s)called\nbound to self id %s\nand id %s\n***'%(
         stack, str(args), str(kwds), str(self), str(self.id)
         )
#
#
#
class _DelegatedMethod(object):
   '''
      idea of this class was lifted from Pyro.core
      i might put a async process here in __call__
      but didn't want to mess with callbks for an example
   '''
   def __init__(self, f, name):
      self.__f = f
      self.__name = name
   def __call__(self, *args, **kwds):
      return self.__f(*args, **kwds)
#
#
#
class CommanderDelegate(object):
   '''
      dynamic delegate for a Commander class
      should make sure its type Commander.
      As long as its a Commander, a sort of Mixin
      would be helpful, following the API. 'with_'
      or whatever was appropriate
   '''
   #
   def __init__(self, commanderClz, *args, **kwds):
      self._dispatchMap = {}
      self._commander = commanderClz(*args, **kwds)
      for m in inspect.getmembers(self._commander):
         if inspect.ismethod(m[1]) and m[0].startswith(self._commander.Prefix):
            self._dispatchMap[m[0]] = m[1]
   #
   def __getattribute__(self, name):
      # the important bits...
      d = object.__getattribute__(self, '_dispatchMap')
      if d.has_key(name):
         return _DelegatedMethod(d[name], name)
      return object.__getattribute__(self, name)
#
#
#
class SharedProctor(SyncManager):
   def __init__(self):
      SyncManager.__init__(self)
      self.register('CommanderProctor', 
            callable=CommanderDelegate, 
            exposed=('with_exposed',))
#
#
#
class MyProcess(multiprocessing.Process):
   #
   def __init__(self, dp=None, dpLock=None):
      multiprocessing.Process.__init__(self)
      self.dp = dp
      self.dpLock = dpLock
   def run(self):
      self.__say()
   def __say(self):
      with self.dpLock:
         s = self.dp.with_exposed()
#     
if __name__ == '__main__':
   
   sp = SharedProctor()
   sp.start()
   cp = sp.CommanderProctor(Commander)
   cpLock = sp.Lock()
   for i in xrange(0,100):
      m = MyProcess(dp=cp, dpLock=cpLock)
      m.start()
      time.sleep(.01)
   
   m.join()
   
