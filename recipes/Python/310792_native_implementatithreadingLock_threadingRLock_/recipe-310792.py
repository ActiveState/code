#### This file is lock.pyx ###
"""This modules natively implements Lock and RLock from the threading module."""

cdef extern from "pythread.h":
    ctypedef void* PyThread_type_lock
    PyThread_type_lock PyThread_allocate_lock()
    void  PyThread_free_lock(PyThread_type_lock lock)
    int PyThread_acquire_lock(PyThread_type_lock lock, int mode)
    void PyThread_release_lock(PyThread_type_lock lock)
    long PyThread_get_thread_ident()

cdef extern from "python.h":
    ctypedef struct PyThreadState:
        # this is a place holder
        pass
    PyThreadState* PyEval_SaveThread()
    void PyEval_RestoreThread(PyThreadState* state)

global WAIT_LOCK
global NO_WAIT_LOCK
WAIT_LOCK = 1
NO_WAIT_LOCK = 0

cdef class Lock:
    """A basic, non-reentrant, Lock."""
    cdef PyThread_type_lock lock
    cdef int locked

    def __new__(self):
        self.lock = PyThread_allocate_lock()
        self.locked=0
    
    def __dealloc__(self):
        PyThread_free_lock(self.lock)
        
    def acquire(self,int mode=1):
        """Lock the lock.  Without argument, this blocks if the lock is already
           locked (even by the same thread), waiting for another thread to release
           the lock, and return None once the lock is acquired.
           With an argument, this will only block if the argument is true,
           and the return value reflects whether the lock is acquired.
           The blocking operation is not interruptible."""
        cdef int result
        cdef PyThreadState* state
        # this is the equivalent of Py_BEGIN_ALLOW_THREADS
        state=PyEval_SaveThread()
        result = PyThread_acquire_lock(self.lock,mode)
        # this is the equivalent of Py_END_ALLOW_THREADS
        PyEval_RestoreThread(state)
        if result==1:
            self.locked = 1
            return True
        else:
            return False
        
    def release(self):
        """Release the lock, allowing another thread that is blocked waiting for
           the lock to acquire the lock.  The lock must be in the locked state,
           but it needn't be locked by the same thread that unlocks it."""
        if self.locked == 0:
            raise Exception('this lock is not locked')
        PyThread_release_lock(self.lock)
        self.locked = 0

cdef class RLock(Lock):
    """A reentrant Lock. It can be locked many times by the same thread."""
    cdef long locker
    
    def acquire(self,int mode=1):
        """Lock the lock.  Without argument, this blocks if the lock is already
           locked (even by the same thread), waiting for another thread to release
           the lock, and return None once the lock is acquired.
           With an argument, this will only block if the argument is true,
           and the return value reflects whether the lock is acquired.
           The blocking operation is not interruptible."""
        cdef long candidate
        cdef int result
        cdef PyThreadState* state

        candidate = PyThread_get_thread_ident()
        if self.locked==0 or candidate!=self.locker:
            state=PyEval_SaveThread()
            result = PyThread_acquire_lock(self.lock,mode)
            PyEval_RestoreThread(state)
            if result==1:
                self.locked = 1
                self.locker = candidate
                return True
            else:
                return False
        else:
            self.locked = self.locked + 1
            return True

    def release(self):
        """Release the lock, allowing another thread that is blocked waiting for
           the lock to acquire the lock.  The lock must be in the locked state,
           but it needn't be locked by the same thread that unlocks it."""
        cdef long candidate
        if self.locked==0:
            raise Exception('this lock is not locked')
        else:
            candidate = PyThread_get_thread_ident()
            if candidate!=self.locker:
                raise Exception('thread %i cannot release lock owned by thread %i'%(candidate,self.locker))
            else:
                self.locked = self.locked - 1
                if self.locked==0:
                    PyThread_release_lock(self.lock)

### This file is setup.py ###
from distutils.core import setup 
from distutils.extension import Extension 
from Pyrex.Distutils import build_ext 
 
setup( 
  name = 'Lock module', 
  ext_modules=[ 
    Extension("lock",         ["lock.pyx"]), 
  ], 
  cmdclass = {'build_ext': build_ext} 
) 
