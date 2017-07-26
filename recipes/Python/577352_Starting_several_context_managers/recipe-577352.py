from __future__ import with_statement

import contextlib
import sys
import threading
import traceback
import unittest


__all__ = ["MultipleError", "parallel"]


class parallel(object):

    """Concurrently start and stop serveral context managers in different
    threads.

    Typical usage::

        with parallel(Foo(), Bar()) as managers:
            foo, bar = managers
            foo.do_something()
            bar.do_something()

    """

    def __init__(self, *managers):
        self.managers = managers

    def __enter__(self):
        errors = []
        threads = []

        for mgr in self.managers:
            t = threading.Thread(target=run,
                                 args=(mgr.__enter__, tuple(), errors))
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()

        if errors:
            err = MultipleError(errors)
            raise err

        return self.managers

    def __exit__(self, *exc_info):
        errors = []
        threads = []

        for mgr in self.managers:
            t = threading.Thread(target=run,
                                 args=(mgr.__exit__, exc_info, errors))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

        if errors:
            raise MultipleError(errors)


class MultipleError(Exception):

    """Exception class to collect several errors in a single object."""

    def __init__(self, errors):
        super(Exception, self).__init__()
        self.errors = errors

    def __str__(self):
        bits = []
        for exc_type, exc_val, exc_tb in self.errors:
            bits.extend(traceback.format_exception(exc_type, exc_val, exc_tb))
        return "".join(bits)


def run(func, args, errors):
    """Helper for ``parallel``.

    """
    try:
        func(*args)
    except:
        errors.append(sys.exc_info())


class ParallelTest(unittest.TestCase):

    def test_parallel(self):
        """Basic tests.

        """
        with parallel(database(), web_server()):
            pass

    def test_errors(self):
        """Tests for errors thrown in context manager methods.

        """
        try:
            with parallel(error_in_enter()):
                pass
        except MultipleError, err:
            self.assertEqual(1, len(err.errors))
            self.assertEqual("enter", str(err.errors[0][1]))

        try:
            with parallel(error_in_exit()):
                pass
        except MultipleError, err:
            self.assertEqual(1, len(err.errors))
            self.assertEqual("exit", str(err.errors[0][1]))

        try:
            with parallel(error_in_enter(), error_in_exit()):
                pass
        except MultipleError, err:
            self.assertEqual(1, len(err.errors))
            self.assertEqual("enter", str(err.errors[0][1]))

        try:
            with parallel(error_in_enter(), error_in_enter()):
                pass
        except MultipleError, err:
            self.assertEqual(2, len(err.errors))
            self.assertEqual("enter", str(err.errors[0][1]))
            self.assertEqual("enter", str(err.errors[1][1]))

        try:
            with parallel(error_in_exit(), error_in_exit()):
                pass
        except MultipleError, err:
            self.assertEqual(2, len(err.errors))
            self.assertEqual("exit", str(err.errors[0][1]))
            self.assertEqual("exit", str(err.errors[1][1]))


@contextlib.contextmanager
def web_server():
    """Sample context manager.

    """
    yield


@contextlib.contextmanager
def database():
    """Sample context manager.

    """
    yield


class error_in_enter(object):

    """Sample context manager."""

    def __enter__(self):
        raise Exception("enter")

    def __exit__(self, *exc_info):
        pass


class error_in_exit(object):

    """Sample context manager."""

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        raise Exception("exit")


if __name__ == "__main__":
    unittest.main()
