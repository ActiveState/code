class QueueInterrupt(Exception):
    pass

class InterruptibleQueue(Queue.Queue):
    """Subclass of Queue allows one to interrupt producers and consumers."""

    def __init__(self,maxsize=0):
        Queue.Queue.__init__(self,maxsize)
        self.consumer_interrupt = False
        self.producer_interrupt = False
    
    def interrupt_all_consumers(self):
        """Raise QueueInterrupt in all consumer threads.

        Any thread currently waiting to get an item, and any subsequent thread
        that calls the get() method, will receive the QueueInterrupt exception.

        """
        self.not_empty.acquire()
        self.consumer_interrupt = True
        self.not_empty.notifyAll()
        self.not_empty.release()
    
    def interrupt_all_producers(self):
        """Raise QueueInterrupt in all producer threads.

        Any thread currently waiting to put an item, and any subsequent thread
        that calls the put() method, will receive the QueueInterrupt exception.

        """
        self.not_full.acquire()
        self.producer_interrupt = True
        self.not_full.notifyAll()
        self.not_full.release()

    def _empty(self):
        if self.consumer_interrupt:
            return False
        return Queue.Queue._empty(self)

    def _full(self):
        if self.producer_interrupt:
            return False
        return Queue.Queue._full(self)

    def _get(self):
        if self.consumer_interrupt:
            raise QueueInterrupt
        return Queue.Queue._get(self)

    def _put(self,item):
        if self.producer_interrupt:
            raise QueueInterrupt
        Queue.Queue._put(self,item)
