"""lock module"""

from time import time, sleep
import threading
import fcntl
from abc import ABCMeta


def wait(delay):
    delay = min(delay*2, .05)
    sleep(delay)
    return delay


class Lock(object):
    """A generic lock object, based on threading.Lock()."""
    __metaclass__ = ABCMeta
    def __init__(self):
        self._locked = False
    def acquire(self, blocking=True, timeout=None):
        if blocking:
            delay = 0.0005
            if timeout is None:
                while self._locked:
                    delay = wait(delay)
            else:
                end = time() + timeout
                while time() < end:
                    if not self._locked:
                        break
                    delay = wait(delay)
                else:
                    return False
            self._locked = True
            return True
        elif timeout is not None:
            raise ValueError("can't specify a timeout "
                             "for a non-blocking call")
        if self._locked:
            return False
        self._locked = True
        return True
    def release(self):
        if not self._locked:
            raise RuntimeError("release unlocked lock")
        self._locked = False
    def locked(self):
        return self._locked

    # for the "with" statement
    def __enter__(self): self.acquire()
    def __exit__(self, *args): self.release()
Lock.register(type(threading.Lock()))


class ThreadingLock(Lock):
    """A subclass of Lock that wraps a threading lock."""
    def __init__(self):
        self._lock = threading.Lock()
    def acquire(self, blocking=True, timeout=None):
        if not blocking and timeout is not None:
            raise ValueError("can't specify a timeout "
                             "for a non-blocking call")
        if timeout is None:
            return self._lock.acquire(blocking)
        else:
            #return self._lock.acquire(blocking, timeout)
            raise NotImplementedError
    def release(self):
        self._lock.release()
    def locked(self):
        return self._lock.locked()


class LockableFile(object):
    """A POSIX file with filesystem locking."""
    def __init__(self, file, mode="r"):
        self._own = False
        if isinstance(file, str):
            file = open(file, mode)
            self._own = True
        self.file = file
        self._locked = False
    def __getattr__(self, name):
        return getattr(self.file, name)
    def lock(self, timeout=3):
        if self._locked:
            return
        # couldn't get lock
        error = None
        end = time() + timeout
        while time() < end:
            try:
                fcntl.lockf(self.file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError, e:
                error = e
                delay = wait(delay)
            else:
                break
        else:
            if error: raise error
        self._locked = True
    def unlock(self):
        fcntl.lockf(self.file, fcntl.LOCK_UN)
        self._locked = False
    def __enter__(self):
        self.lock()
    def __exit__(self, *args):
        self.unlock()
        if self._own:
            self.file.close()


class LockFile(Lock):
    """A Lock subclass implemented on top of a lock file."""
    DEFAULT = "locked"
    def __init__(self, path, value=DEFAULT):
        self.path = path
        self.default = value
    def acquire(self, value=None, blocking=True, timeout=None):
        if value is None:
            value = self.default
        if value is None:
            raise TypeError("missing value")
        try:
            lockfile = LockableFile(self.path, "r+")
        except IOError:
            lockfile = LockableFile(self.path, "a+")
            lockfile.seek(0)
        with lockfile:
            content = lockfile.read()
            #if value is not self.DEFAULT and content == value:
            #    return True
            if not content:
                lockfile.seek(0)
                lockfile.truncate()
                lockfile.write(value)
                return True
            if blocking:
                raise NotImplementedError
            elif timeout is not None:
                raise ValueError("can't specify a timeout "
                                 "for a non-blocking call")
        return False
    def release(self, value=None):
        if value is None:
            value = self.default
        value = str(value)
        try:
            lockfile = LockableFile(self.path, "r+")
        except IOError:
            return
        with lockfile:
            content = lockfile.read()
            if content != value:
                raise RuntimeError("got '%s', expected '%s'" %
                                   (value, content))
            lockfile.seek(0)
            lockfile.truncate()
    def value(self):
        return open(self.path).read()
    locked = value
    def clear(self):
        try:
            lockfile = LockableFile(self.path, "r+")
        except IOError:
            return
        lockfile.truncate()
