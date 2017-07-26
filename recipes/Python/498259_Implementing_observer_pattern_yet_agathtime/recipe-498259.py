"""
observer module

Typical usage is as follows:

from __future__ import with_statement
from observer import consumer, observation

@consumer
def do_something_with_notification():
    while True:
        key, old, new = (yield)
        print "%s: %s -> %s" % (key, old, new)

container = {}

# Any modification to `container`, now called `observed` in the
# body of the with statement, is sent to the coroutine
# do_something_with_notification()

with observation(observe=container,
                 notify=[do_something_with_notification()) as observed:
    modify_observed(observed)

Requires Python 2.5
Author: Jim Baker (jbaker@zyasoft.com)
"""

from __future__ import with_statement
from contextlib import contextmanager
import unittest

@contextmanager
def observation(observe, notify):
    """Simple boilerplate to link to the 'with' statement.

    Contextlib's contextmanager decorator is a very convenient way to
    create simple context managers, specifically the __enter__ and
    __exit__ special methods.
    """

    proxy = Observation(observe, notify)
    try:
        yield proxy
    finally:
        proxy.close()


class NoneSuch(object):
    """A useful alternative to None in the case of a key being deleted or inserted."""
    def __new__(cls, *args, **kwargs):
        if '_inst' not in vars(cls):
            cls._inst = object.__new__(cls, *args, **kwargs)
        return cls._inst
    def __init__(self, *args, **kwargs): pass
    def __repr__(self): return "NoneSuch()"
    def __call__(self, *args, **kwargs): return self
    def __nonzero__(self): return False

NoneSuch = NoneSuch()


class Observation(object):
    """Enables observation of dictionaries.

    Proxies the `observe` dictionary such that any modifications to
    it are sent via `send()` to the notifiers in the `notify`
    sequence.  The sent value is a triple (key, old, new).
    Notifications are sent AFTER the change.

    Other mutable containers, such as sets and lists or your custom
    container, can be readily added by supporting their interface.
    """

    def __init__(self, observe, notify):
        self._obj = observe
        self.notify = notify

    def close(self):
        self._obj = None
        self.notify = None

    def __iter__(self):
        if self._obj is None: raise ValueError("Operation on closed observation")
        return iter(self._obj)

    # all mutating methods go here, this list should be comprehensive as of 2.5
    def __delitem__(self, K):
        if self._obj is None: raise ValueError("Operation on closed observation")
        old = self._obj[K]
        del self._obj[K]
        for notify in self.notify:
            notify.send((K, old, NoneSuch))

    def __setitem__(self, K, V):
        if self._obj is None: raise ValueError("Operation on closed observation")
        old = self._obj.get(K, NoneSuch)
        self._obj[K] = V
        for notify in self.notify:
            notify.send((K, old, V))

    def setdefault(self, K, default):
        if self._obj is None: raise ValueError("Operation on closed observation")
        try:
            return self._obj[K]
        except KeyError:
            self._obj[K] = default
            for notify in self.notify:
                notify.send((K, NoneSuch, default))

    def clear(self):
        if self._obj is None: raise ValueError("Operation on closed observation")
        items = self._obj.items()
        self._obj.clear()
        for K, old in items:
            for notify in self.notify:
                notify.send((K, old, NoneSuch))

    def update(self, *seq_or_map, **kw):
        from itertools import chain

        if self._obj is None: raise ValueError("Operation on closed observation")
        try: seq = seq_or_map[0].iteritems()
        except IndexError: seq = ((K,None) for K in seq_or_map)
        for K, V in chain(seq, kw.iteritems()):
            old = self._obj.get(K, NoneSuch)
            self._obj[K] = V
            for notify in self.notify:
                notify.send((K, old, V))

    def pop(self, K, *default):
        if self._obj is None: raise ValueError("Operation on closed observation")

        # this may be unexpected to have old be the default
        # value. what do you think?
        if default:
            old = self._obj.pop(K, default[0])
        else:
             old = self._obj.pop(K)
        for notify in self.notify:
            notify.send((K, old, NoneSuch))
        return old

    def popitem(self):
        if self._obj is None: raise ValueError("Operation on closed observation")
        K,old = self._obj.popitem()
        for notify in self.notify:
            notify.send((K, old, NoneSuch))
        return old

    def __contains__(self, K):
        if self._obj is None: raise ValueError("Operation on closed observation")
        return K in self._obj
    def __getitem__(self, K):
        if self._obj is None: raise ValueError("Operation on closed observation")
        return self._obj[K]
    def __len__(self):
        if self._obj is None: raise ValueError("Operation on closed observation")
        return len(self._obj)

    # otherwise, just pass through
    def __getattr__(self, attrib):
        if self._obj is None: raise ValueError("Operation on closed observation")
        return getattr(self._obj, attrib)


def consumer(func):
    """A decorator, advances func to its first yield point when called.

    Modifed this original example code from PEP 342 to use the new
    functools.wraps decorator. This convenience function makes it look
    like the original function, which is almost always what we want,
    especially if we designed the original function to be wrapped in
    the first place!

    Maybe `consumer` should go into functools too!
    """

    from functools import wraps

    @wraps(func)
    def wrapper(*args,**kw):
        gen = func(*args, **kw)
        gen.next()
        return gen
    return wrapper



class ObserverTestCase(unittest.TestCase):
    """Tests observer module, special emphasis on dictionary protocol.

    We keep the tests monolithic, just RunTest(), to keep the scope of
    the with statement visible and simple.
    """

    def runTest(self):
        from collections import deque
        changes = deque()

        def consume(X):
            def _consume(X):
                while X:
                    yield X.popleft()
            return list(_consume(X))

        @consumer
        def observe_changes():
            while True:
                change = (yield)
                changes.append(change)

        fruits = dict(apple=1, banana=2, cherry=3)
        with observation(observe=fruits, notify=[observe_changes()]) as observed_fruits:
            # typical mutations
            observed_fruits['cherry'] *= 2
            del observed_fruits['apple']
            self.assertEquals(consume(changes), [('cherry', 3, 6), ('apple', 1, NoneSuch)])

            # .update with keyword args
            observed_fruits.update(durian=4, figs=5)
            self.assertEquals(fruits['durian'], 4)

            # .clear
            observed_fruits.clear()
            self.assertEquals(len(observed_fruits), 0)
            consume(changes) # keep it simple, just throw away

            # .update with map and keyword args, kw should override
            observed_fruits.update({'grapefruit':6, 'jackfruit':7}, jackfruit=8)
            self.assertEquals(observed_fruits['jackfruit'], 8)
            self.assertEquals(consume(changes), [('jackfruit', NoneSuch, 7), ('grapefruit', NoneSuch, 6), ('jackfruit', 7, 8)])

            # .pop, default here may be controversial
            observed_fruits.pop('durian', None)
            self.assertEquals(consume(changes), [('durian', None, NoneSuch)])

            # .setdefault
            observed_fruits.setdefault('jackfruit', -1)
            observed_fruits.setdefault('kiwi', 9)
            self.assertEquals(consume(changes), [('kiwi', NoneSuch, 9)])

            # .popitem
            while observed_fruits:
                observed_fruits.popitem()
            self.assertEquals(fruits, dict())

        # verify that outside of with statement scope, the observation
        # is closed
        self.assertRaises(ValueError, lambda: observed_fruits.update(foo=0, fum=1))


if __name__ == "__main__":
    unittest.main()
