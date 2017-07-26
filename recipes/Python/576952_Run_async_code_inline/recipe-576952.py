import threading
from Queue import Queue

# Set up a queue for tasks to be run on the main thread.
# Most UI toolkits as glib contains functions to push task this way.
Q = Queue()
def idle_add(a,b):
	Q.put((a,b))

def async_int(gen):
    try: gen.next()
    except StopIteration: return
    def do():
        try: gen.next()
        except StopIteration: return
        idle_add(async_int, gen)
    threading.Thread(target=do).start()

def async(func):
    return lambda *a,**kw: async_int(func(*a,**kw))

@async
def test():
    # We start in the main thread
    print "1 %s" % threading.currentThread()
    yield
    
    # This part is run in a seperate thread, not blocking the main thread
    print "2 %s" % threading.currentThread()
    yield
    
    # Now we are back in the main thread
    print "3 %s" % threading.currentThread()
    yield
    
    # And in another background thread
    print "4 %s" % threading.currentThread()
    yield
    
    # And we keep all internal variables between the threads!
    print "5 %s" % threading.currentThread()

if __name__ == "__main__":
    test()
    
    while True:
        a,b = Q.get()
        a(b)
