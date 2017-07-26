#!/usr/bin/env python

"""alarm.py: Permits multiple SIGALRM events to be queued.

Uses a `heapq` to store the objects to be called when an alarm signal is
raised, so that the next alarm is always at the top of the heap.
"""

import heapq
import signal
from time import time

__version__ = '$Revision: 2539 $'.split()[1]

__usage__ = 'usage: %prog [options]'

if __name__ == '__main__':
    import sys
    import optparse
    from random import uniform
    from time import sleep

__alarmlist = []

__new_alarm = lambda t, f, a, k: (t + time(), f, a, k)
__next_alarm = lambda: int(round(__alarmlist[0][0] - time())) if __alarmlist else None
__set_alarm = lambda: signal.alarm(max(__next_alarm(), 1))

def __clear_alarm():
    """Clear an existing alarm.

    If the alarm signal was set to a callable other than our own, queue the
    previous alarm settings.
    """
    oldsec = signal.alarm(0)
    oldfunc = signal.signal(signal.SIGALRM, __alarm_handler)
    if oldsec > 0 and oldfunc != __alarm_handler:
        heapq.heappush(__alarmlist, (__new_alarm(oldsec, oldfunc, [], {})))

def __alarm_handler(*zargs):
    """Handle an alarm by calling any due heap entries and resetting the alarm.

    Note that multiple heap entries might get called, especially if calling an
    entry takes a lot of time.
    """
    try:
        nextt = __next_alarm()
        while nextt is not None and nextt <= 0:
            (tm, func, args, keys) = heapq.heappop(__alarmlist)
            func(*args, **keys)
            nextt = __next_alarm()
    finally:
        if __alarmlist: __set_alarm()

def alarm(sec, func, *args, **keys):
    """Set an alarm.

    When the alarm is raised in `sec` seconds, the handler will call `func`,
    passing `args` and `keys`. Return the heap entry (which is just a big
    tuple), so that it can be cancelled by calling `cancel()`.
    """
    __clear_alarm()
    try:
        newalarm = __new_alarm(sec, func, args, keys)
        heapq.heappush(__alarmlist, newalarm)
        return newalarm
    finally:
        __set_alarm()

def cancel(alarm):
    """Cancel an alarm by passing the heap entry returned by `alarm()`.

    It is an error to try to cancel an alarm which has already occurred.
    """
    __clear_alarm()
    try:
        __alarmlist.remove(alarm)
        heapq.heapify(__alarmlist)
    finally:
        if __alarmlist: __set_alarm()

if __name__ == '__main__':
    optparser = optparse.OptionParser(usage=__usage__, version=__version__)
    optparser.disable_interspersed_args()
    optparser.add_option('--alarms', type='int', metavar='N', default=10,
            help='Number of alarms to create [%default]')
    optparser.add_option('--maxtime', type='float', metavar='SECONDS', default=30,
            help='Maximum time for an alarm [%default sec]')
    (options, args) = optparser.parse_args()

    stime = time()
    etime = stime + options.maxtime
    afunc = lambda x,y,z: sys.stdout.write("Alarm %d time %.2f at %.2f\n" % (x, y, time() - z))
    for a in range(options.alarms):
        atime = uniform(1, options.maxtime)
        aobj = alarm (atime, afunc, a, atime, stime)
        if a == options.alarms / 2: acancel = aobj
    cancel(acancel)
    print "Cancelled alarm %d time %.2f" % (acancel[2][0], acancel[2][1])
    while __alarmlist or time() < etime:
        sleep(1)
