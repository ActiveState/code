import time
from threading import Thread, Condition, Lock
from Queue import Queue, Empty
from functools import partial

class CmdThread(Thread):
  def __init__(self):
    Thread.__init__(self)
    self._queue = Queue()
    self._status = 'NORMAL'
    self._statusLock = Lock()
    self._possibleStatus = ('NORMAL', 'SLEEPING', 'DONE')
    self._condition = Condition(self._statusLock)
    self.daemon = True
    self.start()
 
  def run(self):
    while True:
      self._condition.acquire()
      if self._status == 'DONE':
        self._condition.release()
        break
        
      if self._status == 'SLEEPING':
        self._condition.wait() # this function will release the lock when going to sleep
        self._condition.release()
        continue
      self._condition.release()
      
      try:
        task = self._queue.get_nowait()
      except Empty:
        self._condition.acquire()
        self._status = 'SLEEPING'
        self._condition.wait()
        # Here, we don't change the status to 'NORMAL' here
        # The status is supposed to be changed by the waker
        # Before this command thread wakes up.
        self._condition.release()
        continue

      if callable(task):
        try:
          print 'perform task.'
          task()
        except Exception:
          self._statusLock.acquire()
          self._status = 'DONE'
          self._statusLock.release()
          raise
      else:
        # you can define the task interface here.
        pass
      

  def addCmd(self, callableObj, *args, **argd):
    """ non-blocking call.
    """
    assert(callable(callableObj))
    
    self._condition.acquire()
    if self._status == 'DONE':
      self._condition.release()
      return
    
    self._queue.put(partial(callableObj, *args, **argd))
    self._status = 'NORMAL'
    
    self._condition.notifyAll()
    self._condition.release()

  def close(self, timeout=None):
    """ blocking call, return after close/cancel is done.
    """
    undoneJobs = []
    self._condition.acquire()
    if self._status == 'DONE':
      self._condition.release()
      return
    
    self._status = 'DONE'
    self._condition.notifyAll()
    while not self._queue.empty():
      undoneJobs.append(self._queue.get())
    self._condition.release()
    self.join(timeout)
    return undoneJobs

  def pause(self, timeout=None):
    """ non-blocking call.
    """
    self._condition.acquire()
    if self._status == 'DONE':
      self._condition.release()
      return
    self._status = 'SLEEPING'
    self._condition.notifyAll()
    self._condition.release()

  def resume(self):
    """ non-blocking call.
    """
    self._condition.acquire()
    if self._status == 'DONE':
      self._condition.release()
      return
    self._status = 'NORMAL'
    self._condition.notifyAll()
    self._condition.release()
    
  def hasCmd(self):
    """ non-blocking call.
    """
    return not self._queue.empty()

def demo():
  def exampleTask():
    print 'job beginning...'
    time.sleep(2)
    print 'job finishing...'
  cmdObj = CmdThread()
  for i in xrange(5):
    cmdObj.addCmd(exampleTask)
  return cmdObj

if __name__=='__main__':
  cmd = demo()
  cmd.pause()
  print 'main thread is going to sleep.'
  time.sleep(3)
  print 'main threading is going to close the cmd thread.'
  print cmd.close()
  print 'main thread finishes closing the cmd thread.'
