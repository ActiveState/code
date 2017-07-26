  ## version 1.1, changed according to the suggestions in the comments

  from twisted.internet import reactor, defer
  from twisted.python import threadable; threadable.init(1)
  import sys, time

  ## the wrong way

  def callInThread(func, *args):
      """Takes a blocking function an converts it into a deferred-valued 
      function running in a separate thread.
      """
      de = defer.Deferred()
      de.addCallback(func)
      reactor.callInThread(de.callback, *args)
      return de
  
  deferred = callInThread.__get__ # decorator associated to callInThread

  # the right way
   
  from twisted.internet.threads import deferToThread
  deferred = deferToThread.__get__

  ## example code

  def print_(result):
    print result
  
  def running():
      "Prints a few dots on stdout while the reactor is running."
      sys.stdout.write("."); sys.stdout.flush()
      reactor.callLater(.1, running)

  @deferred
  def sleep(sec):
    "A blocking function magically converted in a non-blocking one."
    print 'start sleep %s' % sec
    time.sleep(sec)
    print '\nend sleep %s' % sec
    return "ok"
  
  if __name__ == "__main__":
     sleep(2).addBoth(print_)
     reactor.callLater(.1, running)
     reactor.callLater(3, reactor.stop)
     reactor.run() 
