"""
A coroutine implementation in Python.

Convert functions to iterator generators by replacing

return <expression>

with

yield <expression>

and function calls: f(*args, **kw) with for loops:

for i in f(*args, **kw):
   pass
# the function value is in i now.

Unfortunately, you have to know which routine has been converted to
an iterator generator and which have not :-(.
"""
from sets import Set
from time import time, sleep
from heapq import heappush, heappop

class coroutine(object):
   def __init__(self, scheduler, function, *args, **kw):
      self.iterator = function(*args, **kw)
      self.scheduler = scheduler
      
   def suspend(self):
      self.scheduler.suspend(self)
      yield None

   def activate(self):
      self.scheduler.activate(self)
      yield None
      
   def sleep(self, sleeptime):
      self.scheduler.sleep(self, sleeptime)
      yield None
      
class scheduler(object):
   """
   Scheduler which runs coroutines in a round robin fashion.
   No priority scheme is implemented.
   """
   def __init__(self):
      self.running = []
      self.running_coroutines = []
      self.running_coroutines_map = {}
      # This data describes the coroutines which are running.
      # self.running contains the next routines to be called.
      # self.running_coroutine maps coroutines to the position
      # in self.running_coroutines

      self.suspended = Set()
      # Coroutines which are not running.
      
      self.waiting_suspend = []
      # Coroutines which are to transition from running to suspended
      
      self.waiting_running = []
      # Coroutines which are to start running
      
      self.waiting_activate = []
      # Coroutines which should switch to the running state.
      
      self.timequeue = []
      # heap of coroutines which are waiting to be activated
      # at a specific time.
      # Entry format: (time, coroutine)
      
      self.event = False
      # Indicates that a state transition should happen.
      
   def add_coroutine(self, coroutine):
      self.suspended.add(coroutine)
      self.activate(coroutine)

   def suspend(self, coroutine):
      self.event = True
      self.waiting_suspend.append(coroutine)
   
   def activate(self, coroutine):
      self.event = True
      self.waiting_activate.append(coroutine)

   def sleep(self, coroutine, sleeptime):
      """
      Sleep for 'sleeptime'.
      """
      item = (time() + sleeptime, coroutine)
      heappush(self.timequeue, item)
      self.suspend(coroutine)
      
   def runat(self, coroutine, runtime):
      """
      Run at a specific time.
      """
      self.sleep(coroutine, sleeptime = runtime - time())
      
   def handle_events(self):
      """
      Handle state transitions from suspended to running
      and vice versa.
      """
      self.event = False
            
      if self.waiting_suspend:
         for c in self.waiting_suspend:
            self.suspended.append(c)

         for c in self.waiting_suspend:
            index = self.running_coroutines_map[c]
            self.remove_coroutine_from_running_list(index)

         self.waiting_suspend = []

      if self.waiting_activate:
         for c in self.waiting_activate:
            self.suspended.remove(c)
            self.running_coroutines_map[c] = len(self.running)
            self.running.append(c.iterator.next)
            self.running_coroutines.append(c)
         self.waiting_activate = []
         
   def remove_coroutine_from_running_list(self, index):
      c = self.running_coroutines[index]
      del self.running[self.index]
      del self.running_coroutines[index]
      del self.running_coroutines_map[c]
      
   def pop_timequeue(self):
      waittime, coroutine = heappop(self.timequeue)
      self.activate(coroutine)
      
   def run(self):
      running = self.running
      running_coroutines = self.running_coroutines
      timequeue = self.timequeue
      
      self.event = True
      while running or timequeue or self.event:
         self.handle_events()

         while running:
            try:
               for self.index, next in enumerate(running):
                  next()
            except StopIteration:
               self.remove_coroutine_from_running_list(self.index)

            while timequeue and timequeue[0][0] <= time():
               self.pop_timequeue()

            if self.event:
               self.handle_events()

         if timequeue:
            sleeptime = timequeue[0][0] - time()
            sleep(sleeptime)
            self.pop_timequeue()

   def current_coroutine(self):
      return self.running_coroutines[self.index]

class semaphore(object):
   """
   Implements a binary semaphore.
   """
   def __init__(self):
      self.free = True
      self.waiting = []
      
   def acquire(self, coroutine):
      if self.free:
         self.free = False
      else:
         coroutine.suspend()
         self.waiting.append(coroutine)

   def release(self):
      if self.waiting:
         coroutine = self.waiting.pop(0)
         coroutine.activate()
      else:
         self.free = True

class monitor(object):
   def __init__(self):
      self.sem = semaphore()

   def run_protected(self, coroutine, function, *args, **kw):
      """
      Call 'function' of 'coroutine'. 'function' is assumed to be a generator function.
      at most one function call of this kind may can be running at any time.
      """
      self.sem.acquire(coroutine)
      try:
         for i in function(*args, **kw):
            pass
         return i
      finally:
         self.sem.release()

current_scheduler = scheduler()
   
def current_coroutine():
   return current_scheduler.current_coroutine()

      
if __name__ == '__main__':
   running = True
   def ack(m, n):
      if not running:
         return
      if m == 0:
         yield n + 1
         return
      if m > 0 and n == 0:
         for i in ack(m-1, 1):
            yield None
         yield i
         return
      if m > 0 and n > 0:
         for i in ack(m, n-1):
            yield None
         t = i
         for i in ack(m-1, t):
            yield None
         yield i
         return

   def a(a1, a2):
      def p(a1, a2):
         print "Ackermann",
         yield None
         print a1,
         yield None
         print a2,
         yield None
         print "=",
         yield None,
         print i
      for i in ack(a1, a2):
         yield None
      print_monitor.run_protected(current_coroutine(), p, a1, a2)

   def watchdog():
      global running
      current_coroutine().sleep(600)
      running = False
      yield None
      
   print_monitor = monitor()
   count = 0
   for i in range(100):
      for j in range(10):
         count += 1
         cr1 = coroutine(current_scheduler, a, 1, i)
         current_scheduler.add_coroutine(cr1)
   for i in range(100):
      for j in range(10):
         count += 1
         cr1 = coroutine(current_scheduler, a, i, j)
         current_scheduler.add_coroutine(cr1)
   current_scheduler.add_coroutine(coroutine(current_scheduler, watchdog))
   print "Starting the run of ", count, "coroutines"
   current_scheduler.run()
