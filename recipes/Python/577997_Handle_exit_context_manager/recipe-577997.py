# Author: Giampaolo Rodola' <g.rodola [AT] gmail [DOT] com>
# License: MIT

from __future__ import with_statement
import contextlib
import signal
import sys


def _sigterm_handler(signum, frame):
    sys.exit(0)
_sigterm_handler.__enter_ctx__ = False


@contextlib.contextmanager
def handle_exit(callback=None, append=False):
    """A context manager which properly handles SIGTERM and SIGINT
    (KeyboardInterrupt) signals, registering a function which is
    guaranteed to be called after signals are received.
    Also, it makes sure to execute previously registered signal
    handlers as well (if any).

    >>> app = App()
    >>> with handle_exit(app.stop):
    ...     app.start()
    ...
    >>>

    If append == False raise RuntimeError if there's already a handler
    registered for SIGTERM, otherwise both new and old handlers are
    executed in this order.
    """
    old_handler = signal.signal(signal.SIGTERM, _sigterm_handler)
    if (old_handler != signal.SIG_DFL) and (old_handler != _sigterm_handler):
        if not append:
            raise RuntimeError("there is already a handler registered for "
                               "SIGTERM: %r" % old_handler)

        def handler(signum, frame):
            try:
                _sigterm_handler(signum, frame)
            finally:
                old_handler(signum, frame)
        signal.signal(signal.SIGTERM, handler)

    if _sigterm_handler.__enter_ctx__:
        raise RuntimeError("can't use nested contexts")
    _sigterm_handler.__enter_ctx__ = True

    try:
        yield
    except KeyboardInterrupt:
        pass
    except SystemExit, err:
        # code != 0 refers to an application error (e.g. explicit
        # sys.exit('some error') call).
        # We don't want that to pass silently.
        # Nevertheless, the 'finally' clause below will always
        # be executed.
        if err.code != 0:
            raise
    finally:
        _sigterm_handler.__enter_ctx__ = False
        if callback is not None:
            callback()


if __name__ == '__main__':
    # ===============================================================
    # --- test suite
    # ===============================================================

    import unittest
    import os

    class TestOnExit(unittest.TestCase):

        def setUp(self):
            # reset signal handlers
            signal.signal(signal.SIGTERM, signal.SIG_DFL)
            self.flag = None

        def tearDown(self):
            # make sure we exited the ctx manager
            self.assertTrue(self.flag is not None)

        def test_base(self):
            with handle_exit():
                pass
            self.flag = True

        def test_callback(self):
            callback = []
            with handle_exit(lambda: callback.append(None)):
                pass
            self.flag = True
            self.assertEqual(callback, [None])

        def test_kinterrupt(self):
            with handle_exit():
                raise KeyboardInterrupt
            self.flag = True

        def test_sigterm(self):
            with handle_exit():
                os.kill(os.getpid(), signal.SIGTERM)
            self.flag = True

        def test_sigint(self):
            with handle_exit():
                os.kill(os.getpid(), signal.SIGINT)
            self.flag = True

        def test_sigterm_old(self):
            # make sure the old handler gets executed
            queue = []
            signal.signal(signal.SIGTERM, lambda s, f: queue.append('old'))
            with handle_exit(lambda: queue.append('new'), append=True):
                os.kill(os.getpid(), signal.SIGTERM)
            self.flag = True
            self.assertEqual(queue, ['old', 'new'])

        def test_sigint_old(self):
            # make sure the old handler gets executed
            queue = []
            signal.signal(signal.SIGINT, lambda s, f: queue.append('old'))
            with handle_exit(lambda: queue.append('new'), append=True):
                os.kill(os.getpid(), signal.SIGINT)
            self.flag = True
            self.assertEqual(queue, ['old', 'new'])

        def test_no_append(self):
            # make sure we can't use the context manager if there's
            # already a handler registered for SIGTERM
            signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))
            try:
                with handle_exit(lambda: self.flag.append(None)):
                    pass
            except RuntimeError:
                pass
            else:
                self.fail("exception not raised")
            finally:
                self.flag = True

        def test_nested_context(self):
            self.flag = True
            try:
                with handle_exit():
                    with handle_exit():
                        pass
            except RuntimeError:
                pass
            else:
                self.fail("exception not raised")

    unittest.main()
