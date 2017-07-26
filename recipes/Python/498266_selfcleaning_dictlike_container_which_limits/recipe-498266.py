'''
self-cleaning time- and size-limited, dict-like container

items are kept in a dict but are also mutually linked to
each other in sequence of their last access time,
from self._oldest to self._newest

cleanup is performed upon each access, proceeding from self._oldest
up to the first one that is not expired yet, so that there is never a need
to iterate over all items; performance of access to single items
should therefore essentially be O(1).

In addition to the time-out, there also is a size limit, which
when exceeded will cause the oldest among the not yet expired items
to be kicked out as well.
'''

from UserDict import DictMixin
import sys
from time import time

class _FakeLock(object):
    '''
    a do-nothin, substituted for a real Lock if there is no threading. Really a micro-optimization.
    '''
    acquire = release = lambda x : None

_FakeLock = _FakeLock() # need only one instance


def RLock():
    '''
    make the container threadsafe if running in a threaded context
    '''
    if 'thread' in sys.modules:     # thread may be imported either directly or by module threading
        import threading
        return threading.RLock()
    else:
        return _FakeLock


class _Item(object):
    '''
    wrapper for items stored in LruDict, providing them with references to one another
    '''
    __slots__ = "key value nextItem previousItem atime".split()
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.nextItem = None
        self.previousItem = None
        self.atime = time()


class LruDict(DictMixin):
    '''
    store up to size items for up to timeout seconds
    We inherit from UserDict.DictMixin rather than from dict
    because DictMixin builds all its methods on a base set
    of user-supplied ones
    '''

    def __init__(self, timeout=600, size=1000, data=None):
        self._lock = RLock()
        self._timeout = timeout
        self._size = size

        # pointers to newest and oldest items
        self._newest = None
        self._oldest = None

        self._data = {}
        if data:
            self.update(data)


    def _setNewest(self, item):
        '''
        put a new or retrieved item at the top of the pile
        '''
        item.atime = time()

        if item is self._newest:                        # item is already on top
            return

        if item.nextItem or item.previousItem:          # this item is currently in the pile...
            self._pullout(item)                         # pull it out

        if self._newest:
            self._newest.nextItem = item                # point the previously newest item to this one...
            item.previousItem = self._newest            # and vice versa

        self._newest = item                             # reset the 'newest' pointer

        if not self._oldest:                            # this only applies if the pile was empty
            self._oldest = item



    def _pullout(self, item):
        '''
        pull an item out of the pile and hook up the neighbours to each other
        '''
        if item is self._oldest:
            if item is self._newest:                    # removing the only item
                self._newest = self._oldest = None
            else:                                       # removing the oldest item of 2 or more
                self._oldest = item.nextItem
                self._oldest.previousItem = None

        elif item is self._newest:                      # removing the newest item of 2 or more
            self._newest = item.previousItem
            self._newest.nextItem = None

        else:   # we are somewhere in between at least 2 others - hitch up the neighbours to each other
            prev = item.previousItem
            next = item.nextItem

            prev.nextItem = next
            next.previousItem = prev

        item.nextItem = item.previousItem = None


    def __setitem__(self, key, value):
        '''
        add a new item or update an old one
        '''
        try:
            self._lock.acquire()
            self.prune()    # here we make a choice - if we prune a the beginning, we may wind up with size+1
                            # items; if we prune at the end, we might keep an expired item. Not serious.

            item = self._data.get(key)
            if item:
                item.value = value
            else:
                item = self._data[key] = _Item(key, value)

            self._setNewest(item)

        finally:
            self._lock.release()


    def __getitem__(self, key):
        '''
        get an item and update its access time and pile position
        '''
        try:
            self._lock.acquire()
            self.prune()
            item = self._data[key]
            self._setNewest(item)
            return item.value

        finally:
            self._lock.release()


    def __delitem__(self, key):
        '''
        delete an item
        '''
        try:
            self._lock.acquire()
            item = self._data.pop(key)
            self._pullout(item)
            self.prune()
        finally:
            self._lock.release()


    def prune(self):
        '''
        called by __delitem__, __getitem__, __setitem__, and _contents
        drop the oldest members until we get back to recent time or
        to size limit
        '''
        if not len(self._data):
            return
        try:
            self._lock.acquire()
            outtime = time() - self._timeout

            while len(self._data) > self._size or self._oldest and self._oldest.atime < outtime:
                drop = self._data.pop(self._oldest.key)
                self._oldest = drop.nextItem
                if self._oldest:
                    self._oldest.previousItem = None

        finally:
            self._lock.release()


    def _contents(self, method, *args):
        '''
        common backend for methods:
        keys, values, items, __len__, __contains__
        '''
        try:
            self._lock.acquire()
            self.prune()

            data = getattr(self._data, method)(*args)
            return data

        finally:
            self._lock.release()


    def __contains__(self, key):
        return self._contents('__contains__', key)

    has_key = __contains__


    def __len__(self):
        return self._contents('__len__')


    def keys(self):
        return self._contents('keys')


    def values(self):
        data = self._contents('values')
        return [v.value for v in data]


    def items(self):
        data = self._contents('items')
        return [(k, v.value) for k, v in data]


    def __repr__(self):
        d = dict(self.items())
        return '%s(timeout=%s, size=%s, data=%s)' % (self.__class__.__name__, self._timeout, self._size, repr(d))


if __name__ == '__main__':

    from time import sleep

    ls = LruDict(timeout=100, size=5)

    print 'expiring items by size'
    l = 10
    for x in range(l):
        ls[x] = ''
        print ls
    print '\nexpiring items by time'

    ls = LruDict(timeout=1, size=100)
    print ls
    for x in xrange(10):
        ls[x] = ''
        print ls
        sleep(0.21)

    size = 10000
    items = 100000
    print '\ncreating a LruDict with length %d and setting %d items' % (size, items)
    ls = LruDict(timeout=600, size=size)
    print ls
    for x in xrange(items):
        ls[x] = ''
    print len(ls)
