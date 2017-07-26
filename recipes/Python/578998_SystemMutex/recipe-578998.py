# License: LGPL
#
# Copyright: Brainwy Software

'''
To use, create a SystemMutex, check if it was acquired (get_mutex_aquired()) and if acquired the
mutex is kept until the instance is collected or release_mutex is called.

I.e.:

mutex = SystemMutex('my_unique_name')
if mutex.get_mutex_aquired():
    print('acquired')
else:
    print('not acquired')
'''

import re
import sys
import tempfile
import traceback
import weakref

# Note: Null comes from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/68205
NULL = Null()


def check_valid_mutex_name(mutex_name):
    # To be windows/linux compatible we can't use non-valid filesystem names
    # (as on linux it's a file-based lock).

    regexp = re.compile(r'[\*\?"<>|/\\:]')
    result = regexp.findall(mutex_name)
    if result is not None and len(result) > 0:
        raise AssertionError('Mutex name is invalid: %s' % (mutex_name,))

if sys.platform == 'win32':

    import os

    class SystemMutex(object):

        def __init__(self, mutex_name):
            check_valid_mutex_name(mutex_name)
            filename = os.path.join(tempfile.gettempdir(), mutex_name)
            try:
                os.unlink(filename)
            except:
                pass
            try:
                handle = os.open(filename, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                try:
                    try:
                        pid = str(os.getpid())
                    except:
                        pid = 'unable to get pid'
                    os.write(handle, pid)
                except:
                    pass  # Ignore this as it's pretty much optional
            except:
                self._release_mutex = NULL
                self._acquired = False
            else:
                def release_mutex(*args, **kwargs):
                    # Note: can't use self here!
                    if not getattr(release_mutex, 'called', False):
                        release_mutex.called = True
                        try:
                            os.close(handle)
                        except:
                            traceback.print_exc()
                        try:
                            # Removing is optional as we'll try to remove on startup anyways (but
                            # let's do it to keep the filesystem cleaner).
                            os.unlink(filename)
                        except:
                            pass

                # Don't use __del__: this approach doesn't have as many pitfalls.
                self._ref = weakref.ref(self, release_mutex)

                self._release_mutex = release_mutex
                self._acquired = True

        def get_mutex_aquired(self):
            return self._acquired

        def release_mutex(self):
            self._release_mutex()


# Below we have a better implementation, but it relies on win32api which we can't be sure
# the client will have available in the Python version installed at the client, so, we're
# using a file-based implementation which should work in any implementation.
#
#     from win32api import CloseHandle, GetLastError
#     from win32event import CreateMutex
#     from winerror import ERROR_ALREADY_EXISTS
#
#     class SystemMutex(object):
#
#         def __init__(self, mutex_name):
#             check_valid_mutex_name(mutex_name)
#             mutex = self.mutex = CreateMutex(None, False, mutex_name)
#             self._acquired = GetLastError() != ERROR_ALREADY_EXISTS
#
#             if self._acquired:
#
#                 def release_mutex(*args, **kwargs):
# Note: can't use self here!
#                     if not getattr(release_mutex, 'called', False):
#                         release_mutex.called = True
#                         try:
#                             CloseHandle(mutex)
#                         except:
#                             traceback.print_exc()
#
# Don't use __del__: this approach doesn't have as many pitfalls.
#                 self._ref = weakref.ref(self, release_mutex)
#                 self._release_mutex = release_mutex
#             else:
#                 self._release_mutex = NULL
#                 CloseHandle(mutex)
#
#         def get_mutex_aquired(self):
#             return self._acquired
#
#         def release_mutex(self):
#             self._release_mutex()

else:  # Linux
    import os
    import fcntl

    class SystemMutex(object):

        def __init__(self, mutex_name):
            check_valid_mutex_name(mutex_name)
            filename = os.path.join(tempfile.gettempdir(), mutex_name)
            try:
                handle = open(filename, 'w')
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except:
                self._release_mutex = NULL
                self._acquired = False
                try:
                    handle.close()
                except:
                    pass
            else:
                def release_mutex(*args, **kwargs):
                    # Note: can't use self here!
                    if not getattr(release_mutex, 'called', False):
                        release_mutex.called = True
                        try:
                            fcntl.flock(handle, fcntl.LOCK_UN)
                        except:
                            traceback.print_exc()
                        try:
                            handle.close()
                        except:
                            traceback.print_exc()
                        try:
                            # Removing is pretty much optional (but let's do it to keep the
                            # filesystem cleaner).
                            os.unlink(filename)
                        except:
                            pass

                # Don't use __del__: this approach doesn't have as many pitfalls.
                self._ref = weakref.ref(self, release_mutex)

                self._release_mutex = release_mutex
                self._acquired = True

        def get_mutex_aquired(self):
            return self._acquired

        def release_mutex(self):
            self._release_mutex()
