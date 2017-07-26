import os, sys, marshal, glob, thread

# Filename used for index files, must not contain numbers
INDEX_FILENAME = 'index'

# Exception thrown when calling get() on an empty queue
class Empty(Exception):  pass

class PersistentQueue:

    def __init__(self, name, cache_size=512, marshal=marshal):
        """
        Create a persistent FIFO queue named by the 'name' argument.

        The number of cached queue items at the head and tail of the queue
        is determined by the optional 'cache_size' parameter.  By default
        the marshal module is used to (de)serialize queue items, but you
        may specify an alternative serialize module/instance with the
        optional 'marshal' argument (e.g. pickle).
        """
        assert cache_size > 0, 'Cache size must be larger than 0'
        self.name = name
        self.cache_size = cache_size
        self.marshal = marshal
        self.index_file = os.path.join(name, INDEX_FILENAME)
        self.temp_file = os.path.join(name, 'tempfile')        
        self.mutex = thread.allocate_lock()
        self._init_index()

    def _init_index(self):
        if not os.path.exists(self.name):
            os.mkdir(self.name)
        if os.path.exists(self.index_file):
            index_file = open(self.index_file)
            self.head, self.tail = map(lambda x: int(x),
                                       index_file.read().split(' '))
            index_file.close()
        else:
            self.head, self.tail = 0, 1
        def _load_cache(cache, num):
            name = os.path.join(self.name, str(num))
            mode = 'rb+' if os.path.exists(name) else 'wb+'
            cachefile = open(name, mode)
            try:
                setattr(self, cache, self.marshal.load(cachefile))
            except EOFError:
                setattr(self, cache, [])
            cachefile.close()
        _load_cache('put_cache', self.tail)
        _load_cache('get_cache', self.head)
        assert self.head < self.tail, 'Head not less than tail'

    def _sync_index(self):
        assert self.head < self.tail, 'Head not less than tail'
        index_file = open(self.temp_file, 'w')
        index_file.write('%d %d' % (self.head, self.tail))
        index_file.close()
        if os.path.exists(self.index_file):
            os.remove(self.index_file)
        os.rename(self.temp_file, self.index_file)

    def _split(self):
        put_file = os.path.join(self.name, str(self.tail))
        temp_file = open(self.temp_file, 'wb')
        self.marshal.dump(self.put_cache, temp_file)
        temp_file.close()
        if os.path.exists(put_file):
            os.remove(put_file)
        os.rename(self.temp_file, put_file)
        self.tail += 1
        if len(self.put_cache) <= self.cache_size:
            self.put_cache = []
        else:
            self.put_cache = self.put_cache[:self.cache_size]
        self._sync_index()

    def _join(self):
        current = self.head + 1
        if current == self.tail:
            self.get_cache = self.put_cache
            self.put_cache = []
        else:
            get_file = open(os.path.join(self.name, str(current)), 'rb')
            self.get_cache = self.marshal.load(get_file)
            get_file.close()
            try:
                os.remove(os.path.join(self.name, str(self.head)))
            except:
                pass
            self.head = current
        if self.head == self.tail:
            self.head = self.tail - 1
        self._sync_index()

    def _sync(self):
        self._sync_index()
        get_file = os.path.join(self.name, str(self.head))
        temp_file = open(self.temp_file, 'wb')
        self.marshal.dump(self.get_cache, temp_file)
        temp_file.close()
        if os.path.exists(get_file):
            os.remove(get_file)
        os.rename(self.temp_file, get_file)
        put_file = os.path.join(self.name, str(self.tail))
        temp_file = open(self.temp_file, 'wb')
        self.marshal.dump(self.put_cache, temp_file)
        temp_file.close()
        if os.path.exists(put_file):
            os.remove(put_file)
        os.rename(self.temp_file, put_file)

    def __len__(self):
        """
        Return number of items in queue.
        """
        self.mutex.acquire()
        try:
            return (((self.tail-self.head)-1)*self.cache_size) + \
                    len(self.put_cache) + len(self.get_cache)
        finally:
            self.mutex.release()

    def sync(self):
        """
        Synchronize memory caches to disk.
        """
        self.mutex.acquire()
        try:
            self._sync()
        finally:
            self.mutex.release()

    def put(self, obj):
        """
        Put the item 'obj' on the queue.
        """
        self.mutex.acquire()
        try:
            self.put_cache.append(obj)
            if len(self.put_cache) >= self.cache_size:
                self._split()
        finally:
            self.mutex.release()

    def get(self):
        """
        Get an item from the queue.
        Throws Empty exception if the queue is empty.
        """
        self.mutex.acquire()
        try:
            if len(self.get_cache) > 0:
                return self.get_cache.pop(0)
            else:
                self._join()
                if len(self.get_cache) > 0:
                    return self.get_cache.pop(0)
                else:
                    raise Empty
        finally:
            self.mutex.release()

    def close(self):
        """
        Close the queue.  Implicitly synchronizes memory caches to disk.
        No further accesses should be made through this queue instance.
        """
        self.mutex.acquire()
        try:
            self._sync()
            if os.path.exists(self.temp_file):
                try:
                    os.remove(self.temp_file)
                except:
                    pass
        finally:
            self.mutex.release()

## Tests
if __name__ == "__main__":
    ELEMENTS = 1000
    p = PersistentQueue('test', 10)
    print 'Enqueueing %d items, cache size = %d' % (ELEMENTS,
                                                    p.cache_size)
    for a in range(ELEMENTS):
        p.put(str(a))
    p.sync()
    print 'Queue length (using __len__):', len(p)
    print 'Dequeueing %d items' % (ELEMENTS/2)
    for a in range(ELEMENTS/2):
        p.get()
    print 'Queue length (using __len__):', len(p)
    print 'Dequeueing %d items' % (ELEMENTS/2)
    for a in range(ELEMENTS/2):
        p.get()
    print 'Queue length (using __len__):', len(p)
    p.sync()
    p.close()
