#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Shared lock (aka reader-writer lock) implementation.
#
# Written by Dmitry Dvoinikov <dmitry@targeted.org>
# Distributed under MIT license.
#
# The latest source code (complete with self-tests) is available from:
# http://www.targeted.org/python/recipes/shared_lock.py
#
# Requires exc_string module available from either
# http://www.targeted.org/python/recipes/exc_string.py -OR-
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/444746
#
# Features:
#
# 1. Supports timeouts. Attempts to acquire a lock occassionally time out in
#    a specified amount of time.
# 2. Fully reentrant - single thread can have any number of both shared and
#    exclusive ownerships on the same lock instance (restricted with the lock 
#    semantics of course).
# 3. Supports FIFO order for threads waiting to acquire the lock exclusively.
# 4. Robust and manageable. Can be created in debug mode so that each lock
#    operation causes the internal invariant to be checked (although this 
#    certainly slows it down). Can be created with logging so that each lock
#    operation is verbosely logged.
# 5. Prevents either side from starvation by picking the winning thread at
#    random if such behaviour is appropriate.
# 6. Recycles temporary one-time synchronization objects.
# 7. Can be used as a drop-in replacement for threading.Lock, ex.
#    >> from shared_lock import SharedLock as Lock
#    because the semantics and exclusive locking interface are identical to 
#    that of threading.Lock.
#
# Synopsis:
#
# class SharedLock(object):
#     def acquire(timeout_sec = None):
#         Attempts to acquire the lock exclusively within the optional timeout.
#         If the timeout is not specified, waits for the lock infinitely.
#         Returns True if the lock has been acquired, False otherwise.
#     def release():
#         Releases the lock previously locked by a call to acquire().
#         Returns None.
#     def acquire_shared(timeout_sec = None):
#         Attempts to acquire the lock in shared mode within the optional
#         timeout. If the timeout is not specified, waits for the lock 
#         infinitely. Returns True if the lock has been acquired, False 
#         otherwise.
#     def release_shared():
#         Releases the lock previously locked by a call to acquire_shared().
#         Returns None.
#
################################################################################
#
# (c) 2005 Dmitry Dvoinikov <dmitry@targeted.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights to 
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
# of the Software, and to permit persons to whom the Software is furnished to do 
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
# THE SOFTWARE.
#
################################################################################

__all__ = [ "SharedLock" ]

################################################################################

from threading import Lock, currentThread, Event
from random import randint
from exc_string import trace_string

if not hasattr(__builtins__, "sorted"):
    def sorted(seq):
        result = [ x for x in seq ]
        result.sort()
        return result

################################################################################

class SharedLock(object):

    def __init__(self, log = None, debug = False):
        """
        Takes two optional parameters, (1) log is an external log function the
        lock would use to send its messages to, ex: lambda s: xprint(s),
        (2) debug is a boolean value, if it's True the lock would be checking
        its internal invariant before and after each call.
        """

        self.__log, self.__debug, self.lckLock = log, debug, Lock()
        self.thrOwner, self.intOwnerDepth, self.dicUsers = None, 0, {}
        self.lstOwners, self.lstUsers, self.lstPooledEvents = [], [], []

    ################################### utility log function

    def _log(self, s):
        thrCurrent = currentThread()
        self.__log("%s @ %.08x %s %s @ %.08x in %s" 
                  % (thrCurrent.getName(), id(thrCurrent), s, 
                     self._debug_dump(), id(self), trace_string()))

    ################################### debugging lock state dump

    def _debug_dump(self):
        return "SharedLock(Ex:[%s] (%s), Sh:[%s] (%s))" \
               % (self.thrOwner is not None 
                  and "%s:%d" % (self.thrOwner.getName(), 
                                 self.intOwnerDepth)
                  or "",
                  ", ".join([ "%s:%d" % (th.getName(), dp)
                              for th, evt, dp in self.lstOwners ]),
                  ", ".join(sorted([ "%s:%d" % (th.getName(), dp)
                                   for th, dp in self.dicUsers.iteritems() ])),
                  ", ".join([ "%s:%d" % (th.getName(), dp)
                              for th, evt, dp in self.lstUsers ]))

    def debug_dump(self):
        """
        Returns a printable string describing the current lock state.
        """

        self._lock()
        try:
            return self._debug_dump()
        finally:
            self._unlock()

    ################################### utility predicates

    def _has_owner(self):
        return self.thrOwner is not None

    def _has_pending_owners(self):
        return len(self.lstOwners) > 0
    
    def _has_users(self):
        return len(self.dicUsers) > 0

    def _has_pending_users(self):
        return len(self.lstUsers) > 0

    ################################### lock invariant

    def _invariant(self): # invariant checks slow down the lock a lot (~3 times)

        # a single thread can hold both shared and exclusive lock
        # as soon as it's the only thread holding either

        if self._has_owner() and self._has_users() \
        and self.dicUsers.keys() != [self.thrOwner]:
            return False

        # if noone is holding the lock, noone should be pending on it

        if not self._has_owner() and not self._has_users():
            return not self._has_pending_owners() \
            and not self._has_pending_users()

        # noone can be holding a lock zero times and vice versa

        if (self._has_owner() and self.intOwnerDepth <= 0) \
        or (not self._has_owner() and self.intOwnerDepth > 0):
            return False

        if len(filter(lambda dp: dp <= 0, self.dicUsers.values())) > 0:
            return False

        # if there is no owner nor pending owners, there should be no
        # pending users (all users must be executing)

        if not self._has_owner() and not self._has_pending_owners() \
        and self._has_pending_users():
            return False

        # if there is no owner nor running users, there should be no
        # pending owners (an owner must be executing)

        if not self._has_owner() and not self._has_users() \
        and self._has_pending_owners():
            return False

        # a thread may be pending on a lock only once, either as user or as owner

        lstPendingThreads = sorted(map(lambda t: t[0], self.lstUsers) + 
                                   map(lambda t: t[0], self.lstOwners))

        for i in range(len(lstPendingThreads) - 1):
            if lstPendingThreads[i] is lstPendingThreads[i+1]:
                return False

        return True 

    ################################### instance lock

    def _lock(self):
        self.lckLock.acquire()

    def _unlock(self):
        self.lckLock.release()

    ################################### sleep/wakeup event pool

    def _pick_event(self):                      # events are pooled/recycled
        if len(self.lstPooledEvents):           # because creating and then
            return self.lstPooledEvents.pop(0)  # garbage collecting kernel
        else:                                   # objects on each call could
            return Event()                      # be prohibitively expensive

    def _unpick_event(self, _evtEvent):
        self.lstPooledEvents.append(_evtEvent)

    ################################### sleep/wakeup utility

    def _acquire_event(self, _evtEvent, timeout): # puts the thread to sleep until the
                                                  # lock is acquired or timeout elapses

        if timeout is None:
            _evtEvent.wait()
            result = True
        else:
            _evtEvent.wait(timeout)
            result = _evtEvent.isSet()

        thrCurrent = currentThread()

        self._lock()
        try:

            # even if result indicates failure, the thread might still be having
            # the lock (race condition between the isSet() and _lock() above)

            if not result:
                result = _evtEvent.isSet()

            # if the lock has not been acquired, the thread must be removed from
            # the pending list it's on. in case the thread was waiting for the
            # exclusive lock and it previously had shared locks, it's put to sleep
            # again this time infinitely (!), waiting for its shared locks back

            boolReAcquireShared = False

            if not result: # the thread has failed to acquire the lock
                
                for i, (thrUser, evtEvent, intSharedDepth) in enumerate(self.lstUsers):
                    if thrUser is thrCurrent and evtEvent is _evtEvent:
                        assert intSharedDepth == 1
                        del self.lstUsers[i]
                        break
                else:
                    for i, (thrOwner, evtEvent, intSharedDepth) in enumerate(self.lstOwners):
                        if thrOwner is thrCurrent and evtEvent is _evtEvent:
                            del self.lstOwners[i]
                            if intSharedDepth > 0:
                                if not self._has_owner():
                                    self.dicUsers[thrCurrent] = intSharedDepth
                                else:
                                    self.lstUsers.append((thrCurrent, _evtEvent, intSharedDepth))
                                    boolReAcquireShared = True
                            break
                    else:
                        assert False, "Invalid thread for %s in %s" % \
                                      (self._debug_dump(), trace_string())

                # if a thread has failed to acquire a lock, it's identical as if it had
                # it and then released, therefore other threads should be released now

                self._release_threads()

            if not boolReAcquireShared:
                _evtEvent.clear()
                self._unpick_event(_evtEvent)

            if self.__debug:
                assert self._invariant(), "SharedLock invariant failed: %s in %s" % \
                                          (self._debug_dump(), trace_string())

            if result:
                if self.__log: self._log("acquired")
            else:
                if self.__log: self._log("timed out in %.02f second(s) waiting for" % timeout)
                if boolReAcquireShared:
                    if self.__log: self._log("acquiring %d previously owned shared lock(s) for" % intSharedDepth)

        finally:
            self._unlock()

        if boolReAcquireShared:
            assert self._acquire_event(_evtEvent, None)
            return False

        return result

    def _release_events(self, _lstEvents): # releases waiting thread(s) 

        for evtEvent in _lstEvents:
            evtEvent.set() 

    ################################### exclusive acquire

    def acquire(self, timeout = None):
        """
        Attempts to acquire the lock exclusively within the optional timeout.
        If the timeout is not specified, waits for the lock infinitely.
        Returns True if the lock has been acquired, False otherwise.
        """

        thrCurrent = currentThread()

        self._lock()
        try:

            if self.__log: self._log("acquiring exclusive")
            if self.__debug:
                assert self._invariant(), "SharedLock invariant failed: %s in %s" % \
                                          (self._debug_dump(), trace_string())

            # this thread already has exclusive lock, the count is incremented

            if thrCurrent is self.thrOwner:

                self.intOwnerDepth += 1
                if self.__debug:
                    assert self._invariant(), "SharedLock invariant failed: %s in %s" % \
                                              (self._debug_dump(), trace_string())
                if self.__log: self._log("acquired exclusive")
                return True

            # this thread already has shared lock, this is the most complicated case

            elif thrCurrent in self.dicUsers:
                
                # the thread gets exclusive lock immediately if there is no other threads

                if self.dicUsers.keys() == [thrCurrent] \
                and not self._has_pending_users() and not self._has_pending_owners():
                    
                    self.thrOwner = thrCurrent
                    self.intOwnerDepth = 1
                    if self.__debug:
                        assert self._invariant(), "SharedLock invariant failed: %s in %s" % \
                                                  (self._debug_dump(), trace_string())
                    if self.__log: self._log("acquired exclusive")
                    return True

                # the thread releases its shared lock in hope for the future
                # exclusive one

                intSharedDepth = self.dicUsers.pop(thrCurrent) # that many times it had shared lock

                evtEvent = self._pick_event()
                self.lstOwners.append((thrCurrent, evtEvent, intSharedDepth)) # it will be given them back

                self._release_threads()

            # a thread acquires exclusive lock whenever there is no
            # current owner nor running users

            elif not self._has_owner() and not self._has_users():

                self.thrOwner = thrCurrent
                self.intOwnerDepth = 1
                if self.__debug:
                    assert self._invariant(), "SharedLock invariant failed: %s in %s" % \
                                              (self._debug_dump(), trace_string())
                if self.__log: self._log("acquired exclusive")
                return True

            # otherwise the thread registers itself as a pending owner with no
            # prior record of holding shared lock

            else: 

                evtEvent = self._pick_event()
                self.lstOwners.append((thrCurrent, evtEvent, 0))

            if self.__debug:
                assert self._invariant(), "SharedLock invariant failed: %s in %s" % \
                                          (self._debug_dump(), trace_string())
            if self.__log: self._log("waiting for exclusive")

        finally:
            self._unlock()

        return self._acquire_event(evtEvent, timeout) # the thread waits for a lock release

    ################################### shared acquire

    def acquire_shared(self, timeout = None):
        """
        Attempts to acquire the lock in shared mode within the optional 
        timeout. If the timeout is not specified, waits for the lock
        infinitely. Returns True if the lock has been acquired, False
        otherwise.
        """

        thrCurrent = currentThread()

        self._lock()
        try:

            if self.__log: self._log("acquiring shared")
            if self.__debug:
                assert self._invariant(), "SharedLock invariant failed: %s in %s" % \
                                          (self._debug_dump(), trace_string())

            # this thread already has shared lock, the count is incremented

            if thrCurrent in self.dicUsers: 
                self.dicUsers[thrCurrent] += 1
                if self.__debug:
                    assert self._invariant(), "SharedLock invariant failed: %s in %s" % \
                                              (self._debug_dump(), trace_string())
                if self.__log: self._log("acquired shared")
                return True

            # this thread already has exclusive lock, now it also has shared

            elif thrCurrent is self.thrOwner: 
                if thrCurrent in self.dicUsers:
                    self.dicUsers[thrCurrent] += 1
                else:
                    self.dicUsers[thrCurrent] = 1
                if self.__debug:
                    assert self._invariant(), "SharedLock invariant failed: %s in %s" % \
                                              (self._debug_dump(), trace_string())
                if self.__log: self._log("acquired shared")
                return True

            # a thread acquires shared lock whenever there is no owner
            # nor pending owners (to prevent owners starvation)

            elif not self._has_owner() and not self._has_pending_owners():
                self.dicUsers[thrCurrent] = 1
                if self.__debug:
                    assert self._invariant(), "SharedLock invariant failed: %s in %s" % \
                                              (self._debug_dump(), trace_string())
                if self.__log: self._log("acquired shared")
                return True

            # otherwise the thread registers itself as a pending user

            else:

                evtEvent = self._pick_event()
                self.lstUsers.append((thrCurrent, evtEvent, 1))

            if self.__debug:
                assert self._invariant(), "SharedLock invariant failed: %s in %s" % \
                                          (self._debug_dump(), trace_string())
            if self.__log: self._log("waiting for shared")

        finally:
            self._unlock()

        return self._acquire_event(evtEvent, timeout) # the thread waits for a lock release

    ################################### 

    def _release_threads(self):

        # a decision is made which thread(s) to awake upon a release

        if self._has_owner():
            boolWakeUpOwner = False # noone to awake, the exclusive owner
            boolWakeUpUsers = False # must've released its shared lock
        elif not self._has_pending_owners():
            boolWakeUpOwner = False
            boolWakeUpUsers = self._has_pending_users()
        elif not self._has_users():
            boolWakeUpOwner = not self._has_pending_users() \
                              or randint(0, 1) == 0 # this prevents starvation
            boolWakeUpUsers = self._has_pending_users() and not boolWakeUpOwner
        else:
            boolWakeUpOwner = False # noone to awake, running users prevent
            boolWakeUpUsers = False # pending owners from running

        # the winning thread(s) are released

        lstEvents = []

        if boolWakeUpOwner:
            self.thrOwner, evtEvent, intSharedDepth = self.lstOwners.pop(0)
            self.intOwnerDepth = 1
            if intSharedDepth > 0:
                self.dicUsers[self.thrOwner] = intSharedDepth # restore thread's shared locks
            lstEvents.append(evtEvent)
        elif boolWakeUpUsers:
            for thrUser, evtEvent, intSharedDepth in self.lstUsers:
                self.dicUsers[thrUser] = intSharedDepth
                lstEvents.append(evtEvent)
            del self.lstUsers[:]

        self._release_events(lstEvents)

    ################################### exclusive release

    def release(self):
        """
        Releases the lock previously locked by a call to acquire().
        Returns None.
        """

        thrCurrent = currentThread()

        self._lock()
        try:

            if self.__log: self._log("releasing exclusive")
            if self.__debug:
                assert self._invariant(), "SharedLock invariant failed: %s in %s" % \
                                          (self._debug_dump(), trace_string())

            if thrCurrent is not self.thrOwner:
                raise Exception("Current thread has not acquired the lock")

            # the thread releases its exclusive lock

            self.intOwnerDepth -= 1
            if self.intOwnerDepth > 0:
                if self.__debug:
                    assert self._invariant(), "SharedLock invariant failed: %s in %s" % \
                                              (self._debug_dump(), trace_string())
                if self.__log: self._log("released exclusive")
                return

            self.thrOwner = None

            # a decision is made which pending thread(s) to awake (if any)

            self._release_threads()
            
            if self.__debug:
                assert self._invariant(), "SharedLock invariant failed: %s in %s" % \
                                          (self._debug_dump(), trace_string())
            if self.__log: self._log("released exclusive")

        finally:
            self._unlock()

    ################################### shared release

    def release_shared(self):
        """
        Releases the lock previously locked by a call to acquire_shared().
        Returns None.
        """

        thrCurrent = currentThread()

        self._lock()
        try:

            if self.__log: self._log("releasing shared")
            if self.__debug:
                assert self._invariant(), "SharedLock invariant failed: %s in %s" % \
                                          (self._debug_dump(), trace_string())

            if thrCurrent not in self.dicUsers:
                raise Exception("Current thread has not acquired the lock")
                
            # the thread releases its shared lock

            self.dicUsers[thrCurrent] -= 1
            if self.dicUsers[thrCurrent] > 0:
                if self.__debug:
                    assert self._invariant(), "SharedLock invariant failed: %s in %s" % \
                                              (self._debug_dump(), trace_string())
                if self.__log: self._log("released shared")
                return
            else:
                del self.dicUsers[thrCurrent]

            # a decision is made which pending thread(s) to awake (if any)

            self._release_threads()
            
            if self.__debug:
                assert self._invariant(), "SharedLock invariant failed: %s in %s" % \
                                          (self._debug_dump(), trace_string())
            if self.__log: self._log("released shared")

        finally:
            self._unlock()

################################################################################
# EOF
