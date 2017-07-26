import threading

class EventQueue(threading.Thread):
    ''' queues function calls, saves their return values in self.return_values.
        >>> eq = EventQueue()    # start a thread watching self.queue
        >>> eq.push(slow_func); eq.push(slow_func, args); eq.push(slow_func, args, kwargs)
        # push some slow [but terminating!] function calls, which will be executed in the order in which they were pushed
        >>> eq.stop()    # stop the thread as soon as the current call returns, possibly preventing some calls from being executed.
    '''
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = []
        self.nap_time = .1
        self.start()
        self.n = 0
        self.serving = None
        self.keep_history = True
        self.return_values = {}    # maps numbers of calls to their return values; unused if not self.keep_history
    
    def error(self, error, function, a=(), kw=None):
        ''' called when function raises error.
        '''
        print >> sys.stderr, 'EventQueue event raised exception (', function, a, kw or {}, '):', error
    
    def push(self, function, a=(), kw=None):
        ''' queue the call to function, return the number of the call.
        '''
        self.queue.append( (function, a, kw or {}) )
        return self.n + len(self.queue)
    
    def stop(self):
        self.running = False
    
    def get(self, n):
        ''' Block until self.n >= n; return whatever the n-th call returned [assuming self.keep_history].
        '''
        while self.n < n:
            time.sleep(self.nap_time)
        return self.return_values.get(n, None)
    
    def run(self):
        ''' a blocking loop which continually calls functions as specified in self.queue.
        '''
        self.running = True
        while self.running:
            if len(self.queue) == 0:
                time.sleep(self.nap_time)
            else:
                function, a, kw = self.queue.pop(0)
                self.serving = (function, a, kw)
                try:
                    if self.keep_history:
                        self.return_values[self.n] = function(*a, **kw)
                    else:
                        function(*a, **kw)
                except Exception, error:
                    self.error(error, function, a, kw)
                self.n += 1



def queue_event(f):
    ''' decorator which queues method/function calls in
        self.eventqueue [if f is a method whose first argument is 'self'],
        otherwise f.eventqueue.
    '''
    args = inspect.getargspec(f)[0]
    if args and (args[0] == 'self'):
        def decorated(self, *a, **kw):
            self.eventqueue.push(f, (self,) + a, kw)
    else:
        f.eventqueue = EventQueue()
        def decorated(*a, **kw):
            f.eventqueue.push(f, a, kw)
    decorated.__name__ = f.__name__
    decorated.__doc__ = f.__doc__
    return decorated
