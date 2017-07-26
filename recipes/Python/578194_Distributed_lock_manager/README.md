## Distributed lock manager for Python  
Originally published: 2012-07-04 20:56:07  
Last updated: 2012-07-04 21:03:32  
Author: pavel   
  
Distributed lock manager provides mutex(es) over network. It is used to synchronize processes running on different machines, e.g. WSGI processes in case of web applications. Lock object is compatible with threading.Lock and can be used as a context manager ("with statement"). It can be easily modified to use UNIX sockets instead of TCP/IP. Communication protocol is text based.

First start server process:

    $ chmod +x dlm.py
    $ ./dlm.py

Usage:

    from dlm import LockClient

    client = LockClient('localhost', 27272, 'client_name')
    
    lock = client.mkLock('lock_name')

    lock.acquire()
    # critical section here...
    lock.release()

    # using context manager
    with lock:
        # critical section here...