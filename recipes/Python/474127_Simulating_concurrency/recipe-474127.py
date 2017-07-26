import types
class method_pseudo_threads(object):
   """
   Implements pseudo threads for class methods.
   """
   _result = None
   
   def __init__(self, caller, instance, *args, **kw):
      self.caller = caller
      self.this_function = self.func(instance, *args, **kw)
      
   def next(self):
      return self.this_function.next()

   def call(self, function, *args, **kwds):
      """
      Check if function is a method of an instance of pseudo_threads.
      If so, call this method via the pseudo_thread mechanism
      """
      special =  hasattr(function, "_parallel")
      if special:
         return (None, function(self.this_function, *args, **kwds))
      else:
         return (function(*args, **kwds), self.this_function)

   def Return(self, value):
      "Return value to the caller"
      return (value, self.caller)
      
   def start(self, thread, *args, **kwds):
      "Start a new pseudo_thread thread, which runs in parallel to the current thread"
      return (None, [self.this_function, thread(None, *args, **kwds)])

   def run(self):
      """
      Calls next for all running threads.
      """
      queue = [self.next()]
      iterations = ticks = 0
      while queue:
         iterations += 1
         newqueue = []
         for result, continuation in queue:
            ticks += 1
            method_pseudo_threads._result = result
            result, continuations = continuation.next()
            if type(continuations) == types.ListType:
               for continuation in continuations:
                  newqueue.append((None, continuation))
            else:
               if continuations:
                     newqueue.append((result, continuations))
         queue = newqueue
      self.iterations, self.ticks = iterations, ticks
      return self._result

def parallel(function):
   """
   Decorator to turn a method into a pseudo_thread.

   The method itself should be written:
   
   def (th, self, *args, **kwds):
      
   Use th.call to call another method which is a pseudo thread.
   Use th.Return to return a value to the caller.
   Use th.start 

   self is the reference to the inclosing instance.
   """
   class p(method_pseudo_threads):
      name = "parallel_class_" + function.func_name
   p.func = function
   def glue(self, caller, *args, **kwds):
      thread = p(caller, self, *args, **kwds)
      yield (None, thread)
   glue._parallel = True
   glue.func_name = "parallel_" + function.func_name
   return glue

class start(method_pseudo_threads):
   def func(self, instance, *args, **kw):
      yield (None, instance)
      yield (None, None)

# Example:

class ackermann(object):
   @parallel
   def acker(th, self, m, n):
      call, Return = th.call, th.Return
      if m == 0:
         yield th.Return(n+1)
      elif m > 0 and n == 0:
         yield call(self.acker, m-1, 1)
         yield Return(th._result)
      elif m > 0 and n > 0:
         yield call(self.acker, m, n-1)
         yield call(self.acker, m-1, th._result)
         yield Return(th._result)
      else:
         assert 0

   @parallel
   def print_ackermann(th, self, m, n):
      yield th.call(self.acker, m, n)
      print "Ackerman(", m, ",", n, ")=", th._result
      yield th.Return(None)
      
   @parallel
   def start(th, self, i, j):
      for i1 in range(i):
         for j1 in range(j):
            yield th.start(self.print_ackermann, i1, j1)
      yield th.Return(None)

def version2():
   ack = ackermann()
   th = ack.start(None, 4, 5)
   start(None, th).run()

if __name__ == '__main__':
   version2()
