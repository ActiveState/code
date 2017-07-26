#!/usr/bin/env python

"""observer.py: A simple, flexible, general-purpose observer pattern.

Observers can be callable objects or objects with a particular named method
(`handle_notify()` by default). Events can be any object, and observers can
select which events they are interested in receiving. Support for a number
of different types of lightweight event objects is included.
"""

import sys
from threading import Lock
from traceback import print_exc

if __name__ == '__main__':
    import optparse

__version__ = '$Revision: 2539 $'.split()[1]

__usage__ = 'usage: %prog [options] [test integer]'


class Observable:
    """Implements a simple observable object.

    Optionally access the observer dictionary in a threadsafe manner. (This
    does not guarantee the thread safety nor order of event notifications!)

    An observer registers for events by calling the `obs_add()` method,
    specifying the event criteria for which the observer wants to be notified.
    An event passed to `_obs_notify()` is checked against the criteria for
    each observer by calling the `_obs_check_event()` method.

    An observer can be a callable object or an object with a particular named
    method (`handle_notify()` by default); when called, the observer is passed
    the observed object and event as arguments.

    Observers must be hashable, as they are stored internally as keys in a
    dictionary.
    """

    def __init__(self, default_notify='handle_notify', threadsafe=False):
        """Construct an observable object.

        The `default_notify` parameter sets the named method to be called
        when sending an event to an observer.
        """
        self._observers = {}
        self._default_notify = default_notify;
        if (threadsafe):
            self.__obs_lock = Lock()
        else:
            self.__obs_lock = None

    def _obs_check_observer(self, observer):
        """Validate an observer and convert it to a callable."""
        if callable(observer):
            return observer
        elif hasattr(observer, self._default_notify):
            return self._obs_check_observer(getattr(observer, self._default_notify))
        else:
            raise TypeError('Object is not a valid observer.')

    def obs_add(self, observer, criteria=None):
        """Add an observer to this object.

        `criteria` specifies the event criteria to listen for. The default
        criteria of `None` listens for all events.

        Observers are stored as strong references to avoid premature garbage
        collection of anonymous observers.
        """
        o_callable = self._obs_check_observer(observer)
        if self.__obs_lock: self.__obs_lock.acquire()
        try:
            self._observers[observer] = [o_callable, criteria]
        finally:
            if self.__obs_lock: self.__obs_lock.release()

    def obs_del(self, observer):
        """Remove an observer from this object."""
        if self.__obs_lock: self.__obs_lock.acquire()
        try:
            del self._observers[observer]
        finally:
            if self.__obs_lock: self.__obs_lock.release()

    # Lambdas for testing whether event matches criteria
    _obs_event_tests = [
        # Event or criteria are None
        lambda a, b, o: (a is None) or (b is None),
        # Event is equal to criteria
        lambda a, b, o: a == b,
        # Event and criteria are bit-field compatible
        lambda a, b, o: (a & b) != 0,
        # Event is a member of criteria
        lambda a, b, o: a in b,
        # If event is subscriptable but not string-like, check event[0] against criteria
        # Try to make sure we don't recurse infinitely
        lambda a, b, o: a != str(a) and a[0] != a \
                and o._obs_check_event(a[0], b),
        # If event is an instance, check event's class against criteria
        # Try to make sure we don't recurse infinitely
        lambda a, b, o: hasattr(a, '__class__') and a.__class__ != a \
                and o._obs_check_event(a.__class__, b)
    ]

    def _obs_check_event(self, event, criteria, tests=_obs_event_tests):
        """Check whether an event meets an observer's criteria.

        The `tests` parameter is a list of callables that take three arguments
        (the event, the criteria, and this object) and return `True` if the
        event meets the criteria.

        The default implementation supports the following event types and
        criteria, and returns `True` if:
        * either the event or criteria is None.
        * the event and criteria support the '&' operation, and
            `event & criteria` is not zero.
        * the event is equal to the criteria or, if the criteria
            is a container, the event is in the criteria.
        * the `__class__` of the event meets the criteria as above
        * if the event is a container, the first element meets the criteria
            as above. This is useful for sending attribute change events as
            tuples of `(<name>, <old value>, <new value>)`, and using a
            sequence of `<name>` as criteria.
        """
        for f in tests:
            try:
                if f(event, criteria, self): return True
            except: pass
        return False

    def _obs_notify(self, event=None):
        """Notify observers of an event if the event meets their criteria.

        If an observer raises an exception, the `_obs_exception()` method is
        called and the observer is removed from the dictionary.
        """
        if self.__obs_lock: self.__obs_lock.acquire()
        try:
            observers = self._observers.items()
        finally:
            if self.__obs_lock: self.__obs_lock.release()
        for o, o_info in observers:
            o_callable, o_criteria = o_info
            if self._obs_check_event(event, o_criteria):
                try:
                    o_callable(self, event)
                except:
                    self._obs_exception()
                    self.obs_del(o)

    def _obs_exception(self):
        """Handle an exception raised by an observer.

        By default, just prints a traceback to `stderr`."""
        print_exc(file=sys.stderr)


if __name__ == '__main__':
    class TestObservable(Observable):
        def run(self, maxbit, testbit=1):
            self._obs_notify(event='start')
            while testbit <= maxbit:
                self._obs_notify(event=testbit)
                self._obs_notify(event=(self, 'tested %d' % testbit))
                testbit *= 2
            self._obs_notify(event='stop')


    class TestObserver:
        def highest_bit(self, x):
            k = 1
            while (x & (x + 1)): x |= (x >> k); k *= 2
            return (x + 1) / 2

        def handle_notify(self, observed, event):
            self.__notifications += 1
            if isinstance(event, tuple): event = event[1]
            print "Notification %d: %s" % (self.__notifications, event)

        def run(self, testval, handler='func', events='bit'):
            observable = TestObservable()
            handlers = { 'func': self.handle_notify, 'obj': self }
            criteria = { 'bit': testval, 'str': ['start','stop'],
                    'tuple': TestObservable, 'all': None }
            observable.obs_add(handlers[handler], criteria[events])
            self.__notifications = 0
            observable.run(self.highest_bit(testval))


    optparser = optparse.OptionParser(usage=__usage__, version=__version__)
    optparser.disable_interspersed_args()
    optparser.add_option('--handler', type='choice', metavar='TYPE',
            choices=['func','obj'], default='func',
            help='Handler type to use: func or obj [%default]')
    optparser.add_option('--events', type='choice', metavar='TYPE',
            choices=['bit','str','tuple','all'], default='bit',
            help='Event type to display: bit, str, tuple, or all [%default]')
    (options, args) = optparser.parse_args()

    if len(args) != 1:
        optparser.print_help()
        sys.exit(1)
    else:
        try:
            TestObserver().run(int(args[0]), handler=options.handler, events=options.events)
        except:
            print_exc(file=sys.stderr)
            optparser.print_help()
            sys.exit(1)
