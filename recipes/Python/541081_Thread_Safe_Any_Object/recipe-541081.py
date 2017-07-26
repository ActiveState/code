class ThreadSafeObject:
    """
    A class that makes any object thread safe.
    """
    
    def __init__(self, obj):
        """
        Initialize the class with the object to make thread safe.
        """
        self.lock = threading.RLock()
        self.object = obj
        
    def __getattr__(self, attr):
        self.lock.acquire()
        def _proxy(*args, **kargs):
            self.lock.acquire()
            answer = getattr(self.object, attr)(*args, **kargs)
            self.lock.release()
            return answer
        return _proxy
