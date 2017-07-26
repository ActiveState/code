"""POSIX (FreeBSD) semaphore bindings."""
from __future__ import with_statement

from ctypes import Structure, POINTER, byref
from ctypes import c_char, c_char_p, c_int, c_size_t, c_uint, c_int32, c_uint32
c_int_p = POINTER(c_int)

EINTR = 4         # Interrupted system call
EEXIST = 17       # Resource temporarily unavailable
EAGAIN = 35       # File exists
ETIMEDOUT = 60    # Operation timed out

def get_func(libname, funcname, restype=None, argtypes=()):
    """Retrieve a function from a library, and set the data types."""
    from ctypes import cdll

    lib = cdll.LoadLibrary(libname)
    func = getattr(lib, funcname)
    func.argtypes = argtypes
    func.restype = restype

    return func

class SemError(RuntimeError):
    """Exception for errors raised by the Sem class."""
    _error = get_func("libc.so", "__error", POINTER(c_int), ())
    _strerror = get_func("libc.so", "strerror", c_char_p, (c_int,))

    def __init__(self):
        """Create an exception based on the value of errno"""
        self.errno = self._error().contents.value
        RuntimeError.__init__(self, self.errno, self._strerror(self.errno))

class c_struct__usem(Structure):
    """FreeBSD provate semaphore structure."""
    _fields_ = (("_has_waiters", c_uint32),
                ("_count", c_uint32),
                ("_flags", c_uint32))

class c_sem(Structure):
    """Semaphore structure."""
    _fields_ = (("_magic", c_uint32),
                ("_kern", c_struct__usem))
c_sem_p = POINTER(c_sem)

class c_struct_timespec(Structure):
    """timespec function."""
    _fields_ = (("tv_sec", c_int32),
                ("tv_nsec", c_int32))
c_struct_timespec_p = POINTER(c_struct_timespec)

class Sem(object):
    """A POSIC semaphore."""
    O_CREAT = 0x0200  # create if nonexistent
    O_EXCL  = 0x0800  # error if already exists

    _clock_gettime = get_func("libc.so", "clock_gettime", None, (c_int32, c_struct_timespec_p))

    _error = get_func("libc.so", "__error", POINTER(c_int), ())

    _sem_close = get_func("libc.so", "sem_close", c_int, (c_sem_p,))
    _sem_destroy = get_func("libc.so", "sem_destroy", c_int, (c_sem_p,))
    _sem_getvalue = get_func("libc.so", "sem_getvalue", c_int, (c_sem_p, c_int_p))
    _sem_init = get_func("libc.so", "sem_init", c_int, (c_sem_p, c_int, c_uint))
    _sem_open = get_func("libc.so", "sem_open", c_sem_p, (c_char_p, c_int))
    _sem_post = get_func("libc.so", "sem_post", c_int, (c_sem_p,))
    _sem_timedwait = get_func("libc.so", "sem_timedwait", c_int, (c_sem_p, c_struct_timespec_p))
    _sem_trywait = get_func("libc.so", "sem_trywait", c_int, (c_sem_p,))
    _sem_unlink = get_func("libc.so", "sem_unlink", c_int, (c_char_p,))
    _sem_wait = get_func("libc.so", "sem_wait", c_int, (c_sem_p,))

    def __init__(self, value=1, name=None, oflags=0x0200):
        """Create a semaphore with initial value, possible name and flags."""
        if name:
            self.sem = None
            self.sem_p = self._sem_open("/%s" % name, oflags)
            if not self.sem_p:
                raise SemError()
        else:
            self.sem = c_sem()
            self.sem_p = c_sem_p(self.sem)
            if self._sem_init(self.sem_p, 0, value):
                raise SemError()

    def __del__(self):
        """Cleanup the semaphore."""
        if self.sem is None:
            res = self._sem_close(self.sem_p)
        else:
            res = self._sem_destroy(self.sem_p)
        if res:
            raise SemError()

    def __len__(self):
        """The current value of the semaphore."""
        return self.getvalue()

    def __enter__(self):
        """Decrement the value of the semaphore, waiting if required."""
        self.wait()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Increment the value of the semaphore."""
        self.post()

    def acquire(self, blocking=True):
        """Decrement the value of the semaphore, block if requested and
        required."""
        if blocking:
            self.wait()
            return True
        else:
            return self.trywait()

    def release(self):
        """Increment the value of the semaphore."""
        self.post()

    def getvalue(self):
        """The current value of the semaphore."""
        from ctypes import c_int, byref

        sval = c_int()
        if self._sem_getvalue(self.sem_p, byref(sval)):
            raise SemError()
        return sval.value

    def post(self):
        """Increment the value of the semaphore."""
        if self._sem_post(self.sem_p):
            raise SemError()

    def timedwait(self, timeout=0, no_eintr=True):
        """Decrement the value of the semaphore, waiting up to timeout if
        required."""
        timespec = c_struct_timespec()
        self._clock_gettime(0, byref(timespec))
        sec = int(timeout)
        nsec = int((timeout - sec) * 1000000000)
        timespec.tv_sec += sec
        timespec.tv_nsec += nsec
        if timespec.tv_nsec >= 1000000000:
            timespec.tv_sec += 1
            timespec.tv_nsec -= 1000000000
        while True:
            if self._sem_timedwait(self.sem_p, byref(timespec)):
                if self._error().contents.value == ETIMEDOUT:
                    return False
                elif not no_eintr or self._error().contents.value != EINTR:
                    raise SemError()
            else:
                return True

    def trywait(self):
        """Decrement the value of the semaphore if possible."""
        if self._sem_trywait(self.sem_p):
            if self._error().contents.value == EAGAIN:
                return False
            else:
                raise SemError()
        return True

    @staticmethod
    def unlink(name):
        """Remove a named semaphore."""
        if Sem._sem_unlink("/%s" % name):
            raise SemError()

    def wait(self, timeout=None, no_eintr=True):
        """Increment the value of the semaphore, wait up to timeout or wait
        indefinitly."""
        if timeout:
            return self.timedwait(timeout, no_eintr)
        while True:
            if self._sem_wait(self.sem_p):
                if not no_eintr or self._error().contents.value != EINTR:
                    raise SemError()
            else:
                return
