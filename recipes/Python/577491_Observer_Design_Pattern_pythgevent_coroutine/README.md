## Observer Design Pattern for python gevent coroutine package  
Originally published: 2010-12-08 08:32:43  
Last updated: 2010-12-08 08:33:30  
Author: Andrey Nikishaev  
  
This is simple implementation of the observer design pattern. Acting as a registration hub, it fires events when requested. \nAlso i have gevent.Timeout like interface in situations when you need to run event-method in the same greenlet. Example: \n\n    e = Observer()\n    ev = e.wait('kill')\n    try:\n        gevent.sleep(3)\n    except FiredEvent:\n        print 'Fired!'\n    else:\n        print 'Not Fired!'\n    finally:\n        ev.cancel() \n\nBut rememeber, if you are using subscribe method, event-method will be executed in another greenlet.\n