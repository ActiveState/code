from datetime import datetime


def timeguard(time_interval, default=None):
    """Run decorated function not often than time_interval.

    If the function is called more often than time_interval
    run the default function instead if it's not None.

    >>> import time
    >>> from datetime import timedelta

    Let's define a test class first:

    >>> class TimeGuardTest(object):
    ...
    ...     def dot(self):
    ...         print ".",
    ...
    ...     @timeguard(timedelta(seconds=3), default=dot)
    ...     def plus(self):
    ...         print "+",
    ...
    ...     @timeguard(timedelta(seconds=2))
    ...     def minus(self):
    ...         print "-",
    ...
    ...     def run(self):
    ...         for i in range(6):
    ...             self.plus()
    ...             self.minus()
    ...             time.sleep(1.1)

    Now run the test and see results:

    >>> test = TimeGuardTest()
    >>> test.run()
    + - . . - + . - .
    """
    def decorator(function):
        # For first time always run the function
        function.__last_run = datetime.min
        def guard(*args, **kwargs):
            now = datetime.now()
            if now - function.__last_run >= time_interval:
                function.__last_run = now
                return function(*args, **kwargs)
            elif default is not None:
                return default(*args, **kwargs)
        return guard
    return decorator


if __name__ == "__main__":
    import doctest
    doctest.testmod()
