######### mrow.py #########

"""Multiple-reader-one-writer resource locking."""

from thread import get_ident
import threading


def acquireLocked(fn):
    def _acquireLocked_wrapper(self, *args, **kw):
        L = self.acquireLock
        try:
            L.acquire()
            result = fn(self, *args, **kw)
        finally:
            L.release()
        return result
    return _acquireLocked_wrapper


def releaseLocked(fn):
    def _releaseLocked_wrapper(self, *args, **kw):
        L = self.releaseLock
        try:
            L.acquire()
            result = fn(self, *args, **kw)
        finally:
            L.release()
        return result
    return _releaseLocked_wrapper


class RWLock(object):
    """MROW resource lock."""

    def __init__(self):
        self.acquireLock = threading.Lock()
        self.releaseLock = threading.Lock()
        self.sublocks = []
        self.waiting = []
        self.readers = 0
        self.writing = False
        self.threadReaders = {}
        self.threadWriters = {}

    def reader(self):
        """Return an acquired read lock."""
        threadReaders, threadWriters = self.threadReaders, self.threadWriters
        ident = get_ident()
        if ident in threadReaders:
            sublock, count = threadReaders[ident]
            threadReaders[ident] = (sublock, count + 1)
            return sublock
        elif ident in threadWriters:
            # Writers are inherently readers, so treat as a reentrant
            # write lock.
            sublock, count = threadWriters[ident]
            threadWriters[ident] = (sublock, count + 1)
            return sublock
        sublock = RLock(self)
        if self.writing:
            # Wait for acquired writers to release.
            self.waiting.append(sublock)
            sublock.acquire()
        sublock.acquire()
        self.readers += 1
        self.sublocks.append(sublock)
        threadReaders[ident] = (sublock, 1)
        return sublock
    reader = acquireLocked(reader)

    def writer(self):
        """Return an acquired write lock."""
        threadReaders, threadWriters = self.threadReaders, self.threadWriters
        ident = get_ident()
        wasReader = False
        if ident in threadWriters:
            sublock, count = threadWriters[ident]
            threadWriters[ident] = (sublock, count + 1)
            return sublock
        elif ident in threadReaders:
            # Readers-turned-writers must wait for any reads to complete
            # before turning into writers.
            sublock, count = threadReaders[ident]
            del threadReaders[ident]
            self.readers -= 1
            self.sublocks.remove(sublock)
            wasReader = True
        sublock = WLock(self)
        if self.readers or self.writing:
            # Wait for acquired readers/writers to release.
            self.waiting.append(sublock)
            sublock.acquire()
        sublock.acquire()
        self.writing = True
        self.sublocks.append(sublock)
        if not wasReader:
            count = 0
        threadWriters[ident] = (sublock, count + 1)
        return sublock
    writer = acquireLocked(writer)

    def _releaseR(self, sublock):
        sublocks = self.sublocks
        if sublock in sublocks:
            threadReaders = self.threadReaders
            ident = get_ident()
            count = threadReaders[ident][1] - 1
            if count:
                threadReaders[ident] = (sublock, count)
            else:
                del threadReaders[ident]
                self.readers -= 1
                sublocks.remove(sublock)
                waiting = self.waiting
                if waiting and not self.readers:
                    # If a lock is waiting at this point, it is a write lock.
                    waiting.pop(0)._release()
    _releaseR = releaseLocked(_releaseR)

    def _releaseW(self, sublock):
        sublocks = self.sublocks
        if sublock in sublocks:
            threadWriters = self.threadWriters
            ident = get_ident()
            count = threadWriters[ident][1] - 1
            if count:
                threadWriters[ident] = (sublock, count)
            else:
                del threadWriters[ident]
                self.writing = False
                sublocks.remove(sublock)
                waiting = self.waiting
                # Release any waiting read locks.
                while waiting and isinstance(waiting[0], RLock):
                    waiting.pop(0)._release()
    _releaseW = releaseLocked(_releaseW)


class SubLock(object):

    def __init__(self, rwlock):
        self.lock = threading.Lock()
        self.rwlock = rwlock

    def _release(self):
        self.lock.release()

    def acquire(self):
        self.lock.acquire()


class RLock(SubLock):

    def release(self):
        self.rwlock._releaseR(self)


class WLock(SubLock):

    def release(self):
        self.rwlock._releaseW(self)



######### test_mrow.py #########


import threading
import time

from schevo.lib import mrow


def writer(L, value, after, rwlock, times):
    """Append value to L after a period of time."""
    try:
        lock = rwlock.writer()
        # Get another lock, to test the fact that obtaining multiple
        # write locks from the same thread context doesn't block (lock
        # reentrancy).
        lock2 = rwlock.writer()
        # Get a reader lock too; should be the same as getting another
        # writer since writers are inherently readers as well.
        lock3 = rwlock.reader()
        times.append(time.time())
        time.sleep(after)
        L.append(value)
    finally:
        times.append(time.time())
        lock3.release()
        lock2.release()
        lock.release()


def reader(L1, L2, after, rwlock, times):
    """Append values from L1 to L2 after a period of time."""
    try:
        lock = rwlock.reader()
        # Get another lock, to test the fact that obtaining multiple
        # write locks from the same thread context doesn't block (lock
        # reentrancy).
        lock2 = rwlock.reader()
        times.append(time.time())
        time.sleep(after)
        L2.extend(L1)
    finally:
        times.append(time.time())
        lock2.release()
        lock.release()


def readerTurnedWriter(L, value, after, rwlock, times):
    """Append value to L after a period of time."""
    try:
        lock = rwlock.reader()
        lock2 = rwlock.writer()
        times.append(time.time())
        time.sleep(after)
        L.append(value)
    finally:
        times.append(time.time())
        lock2.release()
        lock.release()


def test_reentrancy():
    lock = mrow.RWLock()
    # Reentrant read locks.
    rlock1 = lock.reader()
    rlock2 = lock.reader()
    rlock2.release()
    rlock1.release()
    # Reentrant write locks.
    wlock1 = lock.writer()
    wlock2 = lock.writer()
    wlock2.release()
    wlock1.release()
    # Writers are also readers.
    wlock = lock.writer()
    rlock = lock.reader()
    rlock.release()
    wlock.release()


def test_writeReadRead():
    lock = mrow.RWLock()
    W, R1, R2 = [], [], []
    TW, TR1, TR2 = [], [], []
    thread1 = threading.Thread(
        target=writer,
        args=(W, 'foo', 0.2, lock, TW),
        )
    thread2 = threading.Thread(
        target=reader,
        args=(W, R1, 0.2, lock, TR1),
        )
    thread3 = threading.Thread(
        target=reader,
        args=(W, R2, 0.2, lock, TR2),
        )
    thread1.start()
    time.sleep(0.1)
    thread2.start()
    thread3.start()
    time.sleep(0.8)
    assert 'foo' in R1
    assert 'foo' in R2
    assert TR1[0] <= TR2[1]             # Read 1 started during read 2.
    assert TR2[0] <= TR1[1]             # Read 2 started during read 1.
    assert TR1[0] >= TW[1]              # Read 1 started after write.
    assert TR2[0] >= TW[1]              # Read 2 started after write.


def test_writeReadReadWrite():
    lock = mrow.RWLock()
    W, R1, R2 = [], [], []
    TW1, TR1, TR2, TW2 = [], [], [], []
    thread1 = threading.Thread(
        target=writer,
        args=(W, 'foo', 0.3, lock, TW1),
        )
    thread2 = threading.Thread(
        target=reader,
        args=(W, R1, 0.3, lock, TR1),
        )
    thread3 = threading.Thread(
        target=reader,
        args=(W, R2, 0.3, lock, TR2),
        )
    thread4 = threading.Thread(
        target=writer,
        args=(W, 'bar', 0.3, lock, TW2),
        )
    thread1.start()
    time.sleep(0.1)
    thread2.start()
    time.sleep(0.1)
    thread3.start()
    time.sleep(0.1)
    thread4.start()
    time.sleep(1.7)
    assert 'foo' in R1
    assert 'foo' in R2
    assert 'bar' not in R1
    assert 'bar' not in R2
    assert 'bar' in W
    assert TR1[0] <= TR2[1]              # Read 1 started during read 2.
    assert TR2[0] <= TR1[1]              # Read 2 started during read 1.
    assert TR1[0] >= TW1[1]              # Read 1 started after write 1.
    assert TR2[0] >= TW1[1]              # Read 2 started after write 1.
    assert TW2[0] >= TR1[1]              # Write 2 started after read 1.
    assert TW2[0] >= TR2[1]              # Write 2 started after read 2.


def test_writeReadReadtowrite():
    lock = mrow.RWLock()
    W, R1 = [], []
    TW1, TR1, TW2 = [], [], []
    thread1 = threading.Thread(
        target=writer,
        args=(W, 'foo', 0.3, lock, TW1),
        )
    thread2 = threading.Thread(
        target=reader,
        args=(W, R1, 0.3, lock, TR1),
        )
    thread3 = threading.Thread(
        target=readerTurnedWriter,
        args=(W, 'bar', 0.3, lock, TW2),
        )
    thread1.start()
    time.sleep(0.1)
    thread2.start()
    time.sleep(0.1)
    thread3.start()
    time.sleep(1.7)
    assert 'foo' in R1
    assert 'bar' not in R1
    assert 'bar' in W
    assert TR1[0] >= TW1[1]              # Read 1 started after write 1.
    assert TW2[0] >= TR1[1]              # Write 2 started after read 1.
