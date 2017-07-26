import itertools

def retry(delays=(0, 1, 5, 30, 180, 600, 3600),
          exception=Exception,
          report=lambda *args: None):
    def wrapper(function):
        def wrapped(*args, **kwargs):
            problems = []
            for delay in itertools.chain(delays, [ None ]):
                try:
                    return function(*args, **kwargs)
                except exception as problem:
                    problems.append(problem)
                    if delay is None:
                        report("retryable failed definitely:", problems)
                        raise
                    else:
                        report("retryable failed:", problem,
                            "-- delaying for %ds" % delay)
                        time.sleep(delay)
        return wrapped
    return wrapper
