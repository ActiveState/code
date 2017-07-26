## Observer Design Pattern for python gevent coroutine package  
Originally published: 2010-12-08 08:32:43  
Last updated: 2010-12-08 08:33:30  
Author: Andrey Nikishaev  
  
This is simple implementation of the observer design pattern. Acting as a registration hub, it fires events when requested. 
Also i have gevent.Timeout like interface in situations when you need to run event-method in the same greenlet. Example: 

    e = Observer()
    ev = e.wait('kill')
    try:
        gevent.sleep(3)
    except FiredEvent:
        print 'Fired!'
    else:
        print 'Not Fired!'
    finally:
        ev.cancel() 

But rememeber, if you are using subscribe method, event-method will be executed in another greenlet.
