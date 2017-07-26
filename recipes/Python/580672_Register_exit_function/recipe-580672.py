"""
Function / decorator which tries very hard to register a function to
be executed at importerer exit.

Author: Giampaolo Rodola' <g.rodola [AT] gmail [DOT] com>
License: MIT
"""

from __future__ import print_function
import atexit
import os
import functools
import signal
import sys


_registered_exit_funs = set()
_executed_exit_funs = set()


def register_exit_fun(fun=None, signals=[signal.SIGTERM],
                      logfun=lambda s: print(s, file=sys.stderr)):
    """Register a function which will be executed on "normal"
    interpreter exit or in case one of the `signals` is received
    by this process (differently from atexit.register()).
    Also, it makes sure to execute any other function which was
    previously registered via signal.signal(). If any, it will be
    executed after our own `fun`.

    Functions which were already registered or executed via this
    function will be ignored.

    Note: there's no way to escape SIGKILL, SIGSTOP or os._exit(0)
    so don't bother trying.

    You can use this either as a function or as a decorator:

        @register_exit_fun
        def cleanup():
            pass

        # ...or

        register_exit_fun(cleanup)

    Note about Windows: I tested this some time ago and didn't work
    exactly the same as on UNIX, then I didn't care about it
    anymore and didn't test since then so may not work on Windows.

    Parameters:

    - fun: a callable
    - signals: a list of signals for which this function will be
      executed (default SIGTERM)
    - logfun: a logging function which is called when a signal is
      received. Default: print to standard error. May be set to
      None if no logging is desired.
    """
    def stringify_sig(signum):
        if sys.version_info < (3, 5):
            smap = dict([(getattr(signal, x), x) for x in dir(signal)
                         if x.startswith('SIG')])
            return smap.get(signum, signum)
        else:
            return signum

    def fun_wrapper():
        if fun not in _executed_exit_funs:
            try:
                fun()
            finally:
                _executed_exit_funs.add(fun)

    def signal_wrapper(signum=None, frame=None):
        if signum is not None:
            if logfun is not None:
                logfun("signal {} received by process with PID {}".format(
                    stringify_sig(signum), os.getpid()))
        fun_wrapper()
        # Only return the original signal this process was hit with
        # in case fun returns with no errors, otherwise process will
        # return with sig 1.
        if signum is not None:
            if signum == signal.SIGINT:
                raise KeyboardInterrupt
            # XXX - should we do the same for SIGTERM / SystemExit?
            sys.exit(signum)

    def register_fun(fun, signals):
        if not callable(fun):
            raise TypeError("{!r} is not callable".format(fun))
        set([fun])  # raise exc if obj is not hash-able

        signals = set(signals)
        for sig in signals:
            # Register function for this signal and pop() the previously
            # registered one (if any). This can either be a callable,
            # SIG_IGN (ignore signal) or SIG_DFL (perform default action
            # for signal).
            old_handler = signal.signal(sig, signal_wrapper)
            if old_handler not in (signal.SIG_DFL, signal.SIG_IGN):
                # ...just for extra safety.
                if not callable(old_handler):
                    continue
                # This is needed otherwise we'll get a KeyboardInterrupt
                # strace on interpreter exit, even if the process exited
                # with sig 0.
                if (sig == signal.SIGINT and
                        old_handler is signal.default_int_handler):
                    continue
                # There was a function which was already registered for this
                # signal. Register it again so it will get executed (after our
                # new fun).
                if old_handler not in _registered_exit_funs:
                    atexit.register(old_handler)
                    _registered_exit_funs.add(old_handler)

        # This further registration will be executed in case of clean
        # interpreter exit (no signals received).
        if fun not in _registered_exit_funs or not signals:
            atexit.register(fun_wrapper)
            _registered_exit_funs.add(fun)

    # This piece of machinery handles 3 usage cases. register_exit_fun()
    # used as:
    # - a function
    # - a decorator without parentheses
    # - a decorator with parentheses
    if fun is None:
        @functools.wraps
        def outer(fun):
            return register_fun(fun, signals)
        return outer
    else:
        register_fun(fun, signals)
        return fun


# =============================================================================
# tests
# =============================================================================

if __name__ == '__main__':
    import errno
    import subprocess
    import tempfile
    import textwrap
    import unittest

    PY3 = sys.version_info >= (3, 0)
    TESTFN = os.path.join(os.getcwd(), "$testfile")
    POSIX = os.name == 'posix'
    WINDOWS = os.name == 'nt'
    TEST_SIGNALS = [signal.SIGTERM] if POSIX else \
        [signal.CTRL_C_EVENT, signal.CTRL_BREAK_EVENT]
    test_files = []

    def pyrun(src):
        """Run python code 'src' in a separate interpreter.
        Return subprocess exit code.
        """
        if PY3:
            src = bytes(src, 'ascii')
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
            f.write(src)
            f.flush()
            test_files.append(f.name)
            code = subprocess.call(
                [sys.executable, f.name],
                stdout=None, stderr=None,
                # creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        return code

    def safe_remove(file):
        "Convenience function for removing temporary test files"
        try:
            os.remove(file)
        except OSError as err:
            if err.errno != errno.ENOENT:
                raise

    def strfsig(sig):
        smap = dict([(getattr(signal, x), x) for x in dir(signal)
                     if x.isupper() and x.startswith('SIG') and not
                     x.startswith('SIG_')])
        return smap.get(sig, sig)

    class TestRegisterExitFun(unittest.TestCase):

        def setUp(self):
            safe_remove(TESTFN)

        tearDown = setUp

        @classmethod
        def tearDownClass(cls):
            for name in test_files:
                safe_remove(name)

        def test_exit_cleanly(self):
            # Make sure handler fun is called on clean interpreter exit.
            ret = pyrun(textwrap.dedent(
                """
                import os, imp
                mod = imp.load_source("mod", r"{}")

                def foo():
                    with open(r"{}", "ab") as f:
                        f.write(b"1")

                mod.register_exit_fun(foo)
                """.format(os.path.abspath(__file__), TESTFN)
            ))
            self.assertEqual(ret, 0)
            with open(TESTFN, "rb") as f:
                self.assertEqual(f.read(), b"1")

        def test_exception(self):
            # Make sure handler fun is called on exception.
            ret = pyrun(textwrap.dedent(
                """
                import os, imp, sys
                mod = imp.load_source("mod", r"{}")

                def foo():
                    with open(r"{}", "ab") as f:
                        f.write(b"1")

                mod.register_exit_fun(foo)
                sys.stderr = os.devnull
                1 / 0
                """.format(os.path.abspath(__file__), TESTFN)
            ))
            self.assertEqual(ret, 1)
            with open(TESTFN, "rb") as f:
                self.assertEqual(f.read(), b"1")

        def test_signal(self):
            # Make sure handler fun is executed on signal.
            for sig in TEST_SIGNALS:
                safe_remove(TESTFN)
                ret = pyrun(textwrap.dedent(
                    """
                    import os, signal, imp
                    mod = imp.load_source("mod", r"{modname}")

                    def foo():
                        with open(r"{testfn}", "ab") as f:
                            f.write(b"1")

                    mod.register_exit_fun(foo)
                    os.kill(os.getpid(), {sig})
                    """.format(modname=os.path.abspath(__file__),
                               testfn=TESTFN, sig=sig)
                ))
                if POSIX:
                    assert ret == sig, (strfsig(ret), strfsig(sig))
                with open(TESTFN, "rb") as f:
                    self.assertEqual(f.read(), b"1")

        # Skipped on Windows because signal.signal() apparently
        # cannot be used to register functions:
        # http://bugs.python.org/issue26350
        @unittest.skipIf(WINDOWS, "")
        def test_appended_signal(self):
            # Make sure both the old and the new handler funs are
            # executed on signal. New function is supposed to be called
            # first.
            for sig in TEST_SIGNALS:
                safe_remove(TESTFN)
                ret = pyrun(textwrap.dedent(
                    """
                    import os, signal, imp
                    mod = imp.load_source("mod", r"{modname}")

                    def old():
                        with open(r"{testfn}", "ab") as f:
                            f.write(b"old")

                    def new():
                        with open(r"{testfn}", "ab") as f:
                            f.write(b"new")

                    signal.signal({sig}, old)
                    mod.register_exit_fun(new)
                    os.kill(os.getpid(), {sig})
                    """.format(modname=os.path.abspath(__file__), sig=sig,
                               testfn=TESTFN)
                ))
                if POSIX:
                    assert ret == sig, strfsig(ret)
                with open(TESTFN, "rb") as f:
                    data = f.read()
                self.assertEqual(data, b"newold")

        def test_kinterrupt(self):
            # Simulates CTRL + C and make sure the exit function is called.
            ret = pyrun(textwrap.dedent(
                """
                import os, imp, sys
                mod = imp.load_source("mod", r"{}")

                def foo():
                    with open(r"{}", "ab") as f:
                        f.write(b"1")

                mod.register_exit_fun(foo)
                sys.stderr = os.devnull
                raise KeyboardInterrupt
                """.format(os.path.abspath(__file__), TESTFN)
            ))
            self.assertEqual(ret, 1)
            with open(TESTFN, "rb") as f:
                self.assertEqual(f.read(), b"1")

        def test_systemexit(self):
            ret = pyrun(textwrap.dedent(
                """
                import os, imp
                mod = imp.load_source("mod", r"{}")

                def foo():
                    with open(r"{}", "ab") as f:
                        f.write(b"1")

                mod.register_exit_fun(foo)
                raise SystemExit
                """.format(os.path.abspath(__file__), TESTFN)
            ))
            if POSIX:
                self.assertEqual(ret, 0)
            with open(TESTFN, "rb") as f:
                self.assertEqual(f.read(), b"1")

        def test_called_once(self):
            # Make sure the registered fun is called once.
            ret = pyrun(textwrap.dedent(
                """
                import os, imp
                mod = imp.load_source("mod", r"{}")

                def foo():
                    with open(r"{}", "ab") as f:
                        f.write(b"1")

                mod.register_exit_fun(foo)
                """.format(os.path.abspath(__file__), TESTFN)
            ))
            self.assertEqual(ret, 0)
            with open(TESTFN, "rb") as f:
                self.assertEqual(f.read(), b"1")

        def test_cascade(self):
            # Register 2 functions and make sure the last registered
            # function is executed first.
            ret = pyrun(textwrap.dedent(
                """
                import functools, os, imp
                mod = imp.load_source("mod", r"{}")

                def foo(s):
                    with open(r"{}", "ab") as f:
                        f.write(s)

                mod.register_exit_fun(functools.partial(foo, b'1'))
                mod.register_exit_fun(functools.partial(foo, b'2'))
                """.format(os.path.abspath(__file__), TESTFN)
            ))
            self.assertEqual(ret, 0)
            with open(TESTFN, "rb") as f:
                self.assertEqual(f.read(), b"21")

        def test_all_exit_sigs(self):
            # Make sure that functions registered via signal.signal()
            # are executed for all exit signals.
            # Also, make sure our exit function is executed first.
            for sig in TEST_SIGNALS:
                ret = pyrun(textwrap.dedent(
                    """
                    import functools, os, signal, imp
                    mod = imp.load_source("mod", r"{modname}")

                    def foo(s):
                        with open(r"{testfn}", "ab") as f:
                            f.write(s)

                    signal.signal({sig}, functools.partial(foo, b'0'))
                    mod.register_exit_fun(functools.partial(foo, b'1'))
                    mod.register_exit_fun(functools.partial(foo, b'2'))
                    """.format(modname=os.path.abspath(__file__),
                               testfn=TESTFN, sig=sig)
                ))
                if POSIX:
                    self.assertEqual(ret, 0)
                with open(TESTFN, "rb") as f:
                    self.assertEqual(f.read(), b"210")
                safe_remove(TESTFN)

        # Skipped on Windows because signal.signal() apparently
        # cannot be used to register functions:
        # http://bugs.python.org/issue26350
        @unittest.skipIf(WINDOWS, "")
        def test_all_exit_sigs_with_sig(self):
            # Same as above but the process is terminated by a signal
            # instead of exiting cleanly.
            for sig in TEST_SIGNALS:
                ret = pyrun(textwrap.dedent(
                    """
                    import functools, os, signal, imp
                    mod = imp.load_source("mod", r"{modname}")

                    def foo(s):
                        with open(r"{testfn}", "ab") as f:
                            f.write(s)

                    signal.signal({sig}, functools.partial(foo, b'0'))
                    mod.register_exit_fun(functools.partial(foo, b'1'))
                    mod.register_exit_fun(functools.partial(foo, b'2'))
                    os.kill(os.getpid(), {sig})
                    """.format(modname=os.path.abspath(__file__),
                               testfn=TESTFN, sig=sig)
                ))
                self.assertEqual(ret, sig)
                with open(TESTFN, "rb") as f:
                    self.assertEqual(f.read(), b"210")
                safe_remove(TESTFN)

        def test_as_deco(self):
            ret = pyrun(textwrap.dedent(
                """
                import imp
                mod = imp.load_source("mod", r"{}")

                @mod.register_exit_fun
                def foo():
                    with open(r"{}", "ab") as f:
                        f.write(b"1")

                """.format(os.path.abspath(__file__), TESTFN)
            ))
            self.assertEqual(ret, 0)
            with open(TESTFN, "rb") as f:
                self.assertEqual(f.read(), b"1")

        def test_err_in_fun(self):
            # Test that the original signal this process was hit with
            # is not returned in case fun raise an exception. Instead,
            # we're supposed to see retsig = 1.
            ret = pyrun(textwrap.dedent(
                """
                import os, signal, imp, sys
                mod = imp.load_source("mod", r"{}")

                def foo():
                    sys.stderr = os.devnull
                    1 / 0

                sig = signal.SIGTERM if os.name == 'posix' else \
                    signal.CTRL_C_EVENT
                mod.register_exit_fun(foo)
                os.kill(os.getpid(), sig)
                """.format(os.path.abspath(__file__), TESTFN)
            ))
            if POSIX:
                self.assertEqual(ret, 1)
                assert ret != signal.SIGTERM, strfsig(ret)

        def test_as_deco_with_no_parens(self):
            @register_exit_fun
            def foo():
                return 1

            self.assertEqual(foo(), 1)

        def test_as_deco_with_parens(self):
            @register_exit_fun(signals=[signal.SIGINT])
            def foo():
                return 1

            self.assertEqual(foo(), 1)

    unittest.main(verbosity=2)
