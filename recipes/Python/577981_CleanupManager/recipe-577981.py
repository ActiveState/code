import collections
import sys

class CleanupManager(object):
    """Programmatic management of resource cleanup"""
    def __init__(self):
        self._callbacks = collections.deque()

    def register_exit(self, exit):
        """Accepts callbacks with the same signature as context manager __exit__ methods

           Can also suppress exceptions the same way __exit__ methods can.
        """
        self._callbacks.append(exit)
        return exit # Allow use as a decorator

    def register(self, _cb, *args, **kwds):
        """Accepts arbitrary callbacks and arguments. Cannot suppress exceptions."""
        def _wrapper(exc_type, exc, tb):
            _cb(*args, **kwds)
        return self.register_exit(_wrapper)

    def enter_context(self, cm):
        """Accepts and automatically enters other context managers"""
        # We look up the special methods on the type to match the with statement
        _cm_type = type(cm)
        _exit = _cm_type.__exit__
        result = _cm_type.__enter__(cm)
        def _exit_wrapper(*exc_details):
            return _exit(cm, *exc_details)
        self.register_exit(_exit_wrapper)
        return result

    def close(self):
        self.__exit__(None, None, None)

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        if not self._callbacks:
            return
        # This looks complicated, but it is really just
        # setting up a chain of try-expect statements to ensure
        # that outer callbacks still get invoked even if an
        # inner one throws an exception
        def _invoke_next_callback(exc_details):
            # Callbacks are removed from the list in FIFO order
            # but the recursion means they're *invoked* in LIFO order
            cb = self._callbacks.popleft()
            if not self._callbacks:
                # Innermost callback is invoked directly
                return cb(*exc_details)
            try:
                inner_result = _invoke_next_callback(exc_details)
            except:
                cb_result = cb(*sys.exc_info())
                # Check if this cb suppressed the inner exception
                if not cb_result:
                    raise
            else:
                # Check if inner cb suppressed the original exception
                if inner_result:
                    exc_details = (None, None, None)
                cb_result = cb(*exc_details) or inner_result
            return cb_result
        # Kick off the recursive chain
        return _invoke_next_callback(exc_details)
