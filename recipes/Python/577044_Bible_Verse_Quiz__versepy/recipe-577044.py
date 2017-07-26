#! /usr/bin/env python
"""Encapsulate verses from the Bible and support quizzing over them.

The Verse class in this module is far superior to the one implemented in
Java. All quizzing/testing capabilities are imported from another module."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '11 February 2010'
__version__ = '$Revision: 3 $'

################################################################################

import manager
import timeout
import compare

################################################################################

class Verse:

    """Give a helpful interface to the reference and text of a verse.

    The Verse class initially came from TestVerse, written in Java and
    ported into Python. The verse-checking implementation was extremely
    naive and has been reimplemented in another module for this version."""

    __manager = False

    @classmethod
    def init_manager(cls, sleep_interval):
        """Initialize an optional verse-checking management system.

        If a verse is checked with a positive timeout argument, then the
        entry is checked with a timeout. Execution is only guaranteed to
        terminate as the "ready" property is regularly polled. A manager
        initialized here can ensure termination regardless of the client."""
        # This is an optional system. It ensures that timeouts are called.
        # SessionManager(s) cannot be killed, so this is a one-way choice.
        assert not cls.__manager, 'Verse manager is already initialized!'
        cls.__timeout = manager.SessionManager(sleep_interval)
        cls.__timeout.daemon = True
        cls.__timeout.start()
        cls.__manager = True

################################################################################

    def __init__(self, addr, text):
        """Initialize the reference and text of a Verse instance."""
        self.__addr = addr
        self.__text = text
        self.__search = timeout.add_timeout(compare.search)

    def check(self, entry, limit=0, ident=''):
        """Check the entry against the verse's official text.

        Calls with a non-positive limit are blocking in nature. Those with
        a limit greater than zero are started asynchronously and run in a
        separate process. If a timeout manager is running, a cancellation
        method is registered using an IP address and the verse reference."""
        if limit <= 0:
            return compare.search(self.__text, entry)
        # We are working with a timeout call.
        self.__search = timeout.add_timeout(compare.search, limit)
        self.__search(self.__text, entry)
        if Verse.__manager:
            # The verse manager timeout system should be used.
            with Verse.__timeout:
                session = manager.Session(limit + 1, self.__search.cancel)
                Verse.__timeout[ident + ' -> ' + self.__addr] = session

################################################################################

    @property
    def addr(self):
        """Read-only address or reference property."""
        return self.__addr

    @property
    def text(self):
        """Read-only text (from the verse) property."""
        return self.__text

    @property
    def hint(self):
        """Read-only property that computes the hint."""
        return compare.empty_master(self.__text)

    @property
    def ready(self):
        """Read-only status property for a verse check."""
        return self.__search.ready

    @property
    def value(self):
        """Read-only return property for a verse check."""
        return self.__search.value
