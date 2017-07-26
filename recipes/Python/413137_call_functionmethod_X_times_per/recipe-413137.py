def timed_call(callback, calls_per_second, *args, **kw):
    """
    Create an iterator which will call a function a set number
    of times per second.
    """
    time_time = time.time
    start = time_time()
    period = 1.0 / calls_per_second
    while True:
        if (time_time() - start) > period:
            start += period
            callback(*args, **kw)
        yield None
