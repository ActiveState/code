'''
A tagged queue. The producer(s) place items in the queue, each item _may_ have
a list of tags attached to it. Consumer(s) may request an item of a given tag.
The tag is then "consumed" from this item. The item is removed from the queue
when all its tags are consumed.

For better understanding, think about it as set of discinct queues, 
one for a given tag (and one for no tag). 
This will be appropriate for most cases (although internal 
plumbing is different), except for full() which counts all
items regardless of tags to guarrantee maximum object count in memory

If tags are not used, the TaggedQueue behaves exactly as Queue.Queue,
but performance is worse (see below).

Assumptions:
    - tag can be anything that works as a dictionary index
    - when putting an item in the queue, any number of tags can be used,
      but list must be provided (or the tag_list parameter not used at all)
    - when getting an item for the queue, up to 1 tag can be provided. 

Example:

>>> q.put('red only', tag_list=['red'])
>>> q.put('red and blue', tag_list=['red', 'blue'])
>>> q.put('blue only', tag_list=['blue'])
>>> q.put('both colours', tag_list=['red', 'blue'])
>>> q.get(tag='blue')
'red and blue'
>>> q.get(tag='blue')
'blue only'
>>> q.get(tag='red')
'red only'
>>> q.get(tag='red')
'red and blue'
>>> q.get(tag='red')
'both colours'
>>> q.get(tag='blue')
'both colours'


Performance (in seconds, smaller is better):

 - adding an object in the queue 100000 times, then getting it back 100000 times
   (max queue length is 100000)
    Queue.Queue: 1.124342
    TaggedQueue without tags: 5.291548
    TaggedQueue with 10 distinct tags: 2.100272
    TaggedQueue with 1000 distinct tags: 1.692542

 - 100000 consecutive put() - get() calls, (max queue length is 1)
    Queue.Queue: 1.158024
    TaggedQueue without tags: 2.218153
    TaggedQueue with 10 distinct tags: 2.270345
    TaggedQueue with 1000 distinct tags: 2.344355
'''

import multiprocessing
from sys import maxint
from time import time as _time

def id_generator():
    '''a generator returning numeric ID's as identifiers'''
    _id = 0
    while True:
        _id += 1
        if _id == maxint:
            _id = 0
        yield _id

class Empty(Exception):
    '''raised when TaggedQueue is empty for a given tag'''

class Full(Exception):
    '''raised when TaggedQueue is full (regardless of tags)'''

NOTAG = '_notag'

# based on Queue.Queue (no surprise)
class TaggedQueue(object):
    '''A queue similar to Queue.Queue, but producers can tag items
    and consumers can specify what tag are they interested in.
    If an item has multiple tags, it is removed from the queue only after
    all tags attached to it have been consumed.
    '''
    def __init__(self, maxsize=0):
        '''initialize the queue'''
        self.mutex = multiprocessing.Lock()
        self.not_empty = multiprocessing.Condition(self.mutex)
        self.not_full = multiprocessing.Condition(self.mutex)
        self.maxsize = maxsize
        self._tags = {}  # list of refid's for each tag
        self._queue = {}  # the actual queue data
        self._refcount = {}  # how many tags refer to a given refid in the queue
        self.id_generator = id_generator()

    def qsize(self, tag=NOTAG):
        '''Return the approximate size of the queue for a given tag.'''
        self.mutex.acquire()
        try:
            n = len(self._tags[tag])
        except KeyError:
            n = 0
        self.mutex.release()
        return n

    def empty(self, tag=NOTAG):
        '''Return True if the queue is empty for a given tag'''
        self.mutex.acquire()
        n = self._empty(tag)
        self.mutex.release()
        return n

    def full(self):
        '''Return True if the queue is full, regardless of tags'''
        self.mutex.acquire()
        n = self._full() 
        self.mutex.release()
        return n

    def get(self, tag=NOTAG, block=True, timeout=None):
        '''get item object with defined tag from the queue, assuming only
        one tag
        '''
        self.not_empty.acquire()
        try:
            if not block:
                if self._empty(tag):
                    raise Empty
            elif timeout is None:
                while self._empty(tag):
                    self.not_empty.wait()
            else:
                if timeout < 0:
                    raise ValueError("'timeout' must be a positive number")
                endtime = _time() + timeout
                while self._empty(tag):
                    remaining = endtime - _time()
                    if remaining <= 0.0:
                        raise Empty
                    self.not_empty.wait(remaining)
            item = self._get(tag)
            self.not_full.notify()
            return item
        finally:
            self.not_empty.release()

    def get_nowait(self, tag=NOTAG):
        '''get tagged item immediatelly or raise an exception'''
        return self.get(tag, block=False)
    
    def put(self, item, tag_list=[NOTAG], block=True, timeout=None):
        '''put an item in queue, tag_list is an optional list of tags
        to be attached to the item
        '''
        self.not_full.acquire()
        try:
            if not block:
                if self._full():
                    raise Full
            elif timeout is None:
                while self._full():
                    self.not_full.wait()
            else:
                if timeout < 0:
                    raise ValueError("'timeout' must be a positive number")
                endtime = _time() + timeout
                while self._full():
                    remaining = endtime - _time()
                    if remaining <= 0.0:
                        raise Full
                    self.not_full.wait(remaining)
            self._put(item, tag_list)
            self.not_empty.notify()
        finally:
            self.not_full.release()

    def put_nowait(self, item, tag_list=[NOTAG]):
        '''put an item to the list immediatelly or raise an exception'''
        return self.put(item, tag_list, False)

    def _empty(self, tag):
        return not (tag in self._tags)

    def _full(self):
        return self.maxsize > 0 and len(self._refcount) == self.maxsize 

    def _get(self, tag):
        if not tag in self._tags:
            raise Empty
        # get item's refid of the item
        refid = self._tags[tag].pop(0)  # get and remove first item from list
        if not self._tags[tag]:  # no item in the queue have this tag anymore
            del(self._tags[tag])
        # get the item from the queue
        item = self._queue[refid]
        # decrease the reference counter
        self._refcount[refid] -= 1
        if self._refcount[refid] == 0:  # no more references
            del self._refcount[refid]
            del self._queue[refid]
        return item

    def _put(self, item, tag_list):
        refid = self.id_generator.next()
        self._queue[refid] = item
        self._refcount[refid] = len(tag_list)
        for t in tag_list:
            try:
                self._tags[t].append(refid)
            except KeyError:
                self._tags[t] = [refid]

## --- test_tagged_queue.py

'''
Test that TaggedQueue works as expected
'''

from tagged_queue import TaggedQueue, Empty

def test_empty_queue():
    '''test that TaggedQueue returns Empty correctly'''
    q = TaggedQueue()
    try:
        q.get_nowait()
        assert False
    except Empty:
        pass
    
    try:
        q.get_nowait(tag='non_existing')
        assert False
    except Empty:
        pass

def test_put_and_get():
    '''test that tags are honoured for basic queue operations'''
    q = TaggedQueue()
    q.put_nowait('no tag')
    assert q.get_nowait() == 'no tag'
    q.put_nowait('test data', tag_list=['tag1', 'tag2', 3])
    try:
        q.get_nowait()
        assert False
    except Empty:
        pass
    q.get_nowait(tag=3)
    q.get_nowait(tag='tag1')
    q.get_nowait(tag='tag2')
    try:
        q.get_nowait(tag='tag2')
        assert False
    except Empty:
        pass

def test_empty():
    '''test that .empty() function works as expected'''
    q = TaggedQueue()
    assert q.empty()
    assert q.empty(tag='tag1')
    q.put_nowait('test data')
    assert not q.empty()
    assert q.empty(tag='tag1')
    q.put_nowait('other test data', tag_list=['tag1'])
    assert not q.empty()
    assert not q.empty(tag='tag1')
    q.get_nowait()
    assert q.empty()
    assert not q.empty(tag='tag1')
    q.get_nowait(tag='tag1')
    assert q.empty()
    assert q.empty('tag1')

def test_qsize():
    '''test that .qsize() function works as expected'''
    q = TaggedQueue()
    assert q.qsize() == 0
    assert q.qsize(tag='tag1') == 0
    q.put_nowait('test data')
    assert q.qsize() == 1
    assert q.qsize(tag='tag1') == 0
    q.put_nowait('other test data', tag_list=['tag1'])
    assert q.qsize() == 1
    assert q.qsize(tag='tag1') == 1
    q.put_nowait('other test data', tag_list=['tag1'])
    assert q.qsize() == 1
    assert q.qsize(tag='tag1') == 2
    q.get_nowait()
    assert q.qsize() == 0
    assert q.qsize(tag='tag1') == 2
    q.get_nowait(tag='tag1')
    assert q.qsize() == 0
    assert q.qsize(tag='tag1') == 1
    q.get_nowait(tag='tag1')
    assert q.qsize() == 0
    assert q.qsize(tag='tag1') == 0

def test_full():
    '''test that .full() function works as expected'''
    q = TaggedQueue(maxsize=3)
    assert not q.full()
    q.put_nowait('data')
    assert not q.full()
    q.put_nowait('other data', tag_list=['some_tag'])
    assert not q.full()
    q.put_nowait('yet another data')
    assert q.full()

def test_ordering():
    '''test that queue ordering works properly'''
    q = TaggedQueue()
    q.put_nowait('red only', tag_list=['red'])
    q.put_nowait('red and blue', tag_list=['red', 'blue'])
    q.put_nowait('blue only', tag_list=['blue'])
    q.put_nowait('both colours', tag_list=['red', 'blue'])
    assert q.get_nowait(tag='blue') == 'red and blue'
    assert q.get_nowait(tag='blue') == 'blue only'
    assert q.get_nowait(tag='red') == 'red only'
    assert q.get_nowait(tag='red') == 'red and blue'
    assert q.get_nowait(tag='red') == 'both colours'
    assert q.get_nowait(tag='blue') == 'both colours'
