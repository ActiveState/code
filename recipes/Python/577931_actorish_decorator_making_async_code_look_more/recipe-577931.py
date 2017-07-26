from threading import Thread, Lock
from peak.util.proxies import LazyProxy

def function_thread(f, lock=None):
    def args_wrapper(*args, **kwargs):
        class FunctionRunner(Thread):
            def run(self):
                if lock is not None: lock.acquire()
                try:
                    self.result = f(*args, **kwargs)
                finally:
                    if lock is not None: lock.release()
        t = FunctionRunner()
        t.start()
        def callback():
            t.join()
            return t.result 
        proxy = LazyProxy(callback)
        return proxy
    return args_wrapper
                
from time import sleep

@function_thread
def power(a, b):
    print 'looong power operation', a
    sleep(a)
    return a ** b

result10_10 = power(1, 10)
result20_20 = power(2, 20)
result30_30 = power(3, 30)
result40_40 = power(4, 40)

sleep(1)
print '\nresult 1**10 = ', result10_10,\
      '\nresult 2**20 = ', result20_20,\
      '\nresult 3**30 = ', result30_30,\
      '\nresult 4**40 = ', result40_40, '\n\n'

##############################
import socket

urls = ['www.google.com', 'www.example.com', 
        'www.python.org', 'code.activestate.com']
def gethostbyname(*args, **kwargs):
    print 'sleeping...',
    sleep(2) # makes gethostbyname take a looong time
    return socket.gethostbyname(*args, **kwargs)
##############################
gethostbyname_threaded = function_thread(gethostbyname)
results = []
for url in urls:
    results.append(gethostbyname_threaded(url))
    print 'url appended', url
print '\ndoing some other stuff'
sleep(2)
print '\npar results =', results

##############################
gethostbyname_locked = function_thread(gethostbyname, lock=Lock())
results = []
for url in urls:
    results.append(gethostbyname_locked(url))
print '\nseq results =', results
