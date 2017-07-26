#! /usr/bin/env python
"""Oversee the timely destruction of unused sessions.

The two classes in this module allow automated memory cleanup to be regularly
performed and timed actions to be executed within reasonable time periods."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '11 February 2010'
__version__ = '$Revision: 3 $'

################################################################################

import threading
import time

################################################################################

class SessionManager(threading.Thread, threading._RLock, dict):

    """Manage session objects along with associated data.

    This class acts as dictionary with a data-protection mutex.
    It can run a cleanup routine at regular intervals if needed."""

    def __init__(self, sleep_interval):
        """Initialize variables in SessionManager's parent classes."""
        threading.Thread.__init__(self)
        threading._RLock.__init__(self)
        self.__sleep_interval = sleep_interval
    
    def run(self):
        """Remove old sessions from memory as needed.

        This method is executed by calling .start() on a SessionManager
        object. The "daemon" attribute may need be set to True before
        activating this feature. Please note that once this cleanup
        routine begins, it must run until the program terminates."""
        while True:
            time.sleep(self.__sleep_interval)
            with self:
                for key in tuple(self):
                    if not super().__getitem__(key):
                        del self[key]

    def __setitem__(self, key, value):
        """Add manager attribute to value before storing it."""
        value.manager = self
        super().__setitem__(key, value)

    def __getitem__(self, key):
        """Retrieve the session specified by the given key.

        Like a normal dictionary, the value is returned to the caller
        if it was found. However, the wakeup method on the session is
        called first. This effectively delays the session's deletion."""
        session = super().__getitem__(key)
        session.wakeup()
        return session

    def __hash__(self):
        """Compute a hash as required by Thread objects."""
        return id(self)

################################################################################

class Session:

    """Store session variables for a limited time period.

    The only functionality this class directly supports is calling an event
    handler when the instance is destroyed. Session objects given to a
    SessionManager are automatically cleared out of memory when their "time to
    live" is exceeded. The manager must be started for such functionality."""

    def __init__(self, time_to_live, on_destroyed=None):
        """Initialize timeout setting and deletion handler."""
        self.__time_to_live = time_to_live
        self.__on_destroyed = on_destroyed
        self.wakeup()

    def wakeup(self):
        """Refresh the last-accessed time of this session object.

        This method is automatically called by the class initializer.
        Instances also get a wakeup call when retrieved from a manager."""
        self.__time = time.time()

    def __bool__(self):
        """Calculate liveliness of object for manager."""
        return time.time() - self.__time <= self.__time_to_live

    def __del__(self):
        """Call deletion event handler if present.

        Completely optional: an on_destroyed handler may be specified
        when the object is created. Exception handling is non-existent."""
        if self.__on_destroyed is not None:
            self.__on_destroyed()
