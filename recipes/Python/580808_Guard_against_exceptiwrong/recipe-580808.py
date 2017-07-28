from functools import wraps

class exception_guard(object):
    """Guard against the given exception and raise a different exception."""

    def __init__(self, catchable, throwable=RuntimeError):
        if is_exception_class(catchable):
            self._catchable = catchable
        else:
            raise TypeError('catchable must be one or more exception types')
        if throwable is None or is_exception(throwable):
            self._throwable = throwable
        else:
            raise TypeError('throwable must be None or an exception')

    def throw(self, cause):
        """Throw an exception from the given cause."""
        throwable = self._throwable
        assert throwable is not None
        self._raisefrom(throwable, cause)

    def _raisefrom(self, exception, cause):
        # "raise ... from ..." syntax only supported in Python 3.
        assert cause is not None  # "raise ... from None" is not supported.
        if isinstance(exception, BaseException):
            # We're given an exception instance, so just use it as-is.
            pass
        else:
            # We're given an exception class, so instantiate it with a
            # helpful error message.
            assert issubclass(exception, BaseException)
            name = type(cause).__name__
            message = 'guard triggered by %s exception' % name
            exception = exception(message)
        try:
            exec("raise exception from cause", globals(), locals())
        except SyntaxError:
            # Python too old. Fall back to a simple raise, without cause.
            raise exception

    # === Context manager special methods ===

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None and issubclass(exc_type, self._catchable):
            if self._throwable is None:
                # Suppress the exception.
                return True
            else:
                self.throw(exc_value)

    # === Use exception_guard as a decorator ===

    def __call__(self, function):
        catchable = self._catchable
        suppress_exception = (self._throwable is None)
        @wraps(function)
        def inner(*args, **kwargs):
            try:
                result = function(*args, **kwargs)
            except catchable as error:
                if suppress_exception:
                    return
                else:
                    self.throw(error)
            else:
                return result
        return inner


# Two helper functions.

def is_exception(obj):
    """Return whether obj is an exception.

    >>> is_exception(ValueError)  # An exception class.
    True
    >>> is_exception(ValueError())  # An exception instance.
    True
    >>> is_exception(float)
    False

    """
    try:
        return issubclass(obj, BaseException)
    except TypeError:
        return isinstance(obj, BaseException)

def is_exception_class(obj):
    """Return whether obj is an exception class, or a tuple of the same.

    >>> is_exception_class(ValueError)
    True
    >>> is_exception_class(float)
    False
    >>> is_exception_class(ValueError())  # An instance, not a class.
    False
    >>> is_exception_class((ValueError, KeyError))
    True

    """
    try:
        if isinstance(obj, tuple):
            return obj and all(issubclass(X, BaseException) for X in obj)
        return issubclass(obj, BaseException)
    except TypeError:
        return False
