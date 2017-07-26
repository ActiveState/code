# Simple version:

import sys, time

class RetryError(Exception):
    pass

def retryloop(attempts, timeout):
    starttime = time.time()
    success = set()
    for i in range(attempts): 
        success.add(True)
        yield success.clear
        if success:
            return
        if starttime + timeout < time.time():
            break
    raise RetryError

""" 
Usage:

for retry in retryloop(10, timeout=30):
    try:
        something
    except SomeException:
        retry()

for retry in retryloop(10, timeout=30):
    something
    if somecondition:
        retry()

"""

# Fancy version:

def fancyretryloop(attempts, timeout=None, delay=0, backoff=1):
    starttime = time.time()
    success = set()
    for i in range(attempts): 
        success.add(True)
        yield success.clear
        if success:
            return
        duration = time.time() - starttime
        if timeout is not None and duration > timeout:
            break
        if delay:
            time.sleep(delay)
            delay = delay * backoff

    e = sys.exc_info()[1]

    # No pending exception? Make one
    if e is None:
        try: raise RetryError
        except RetryError as e: pass

    # Decorate exception with retry information:
    e.args = e.args + ("on attempt {0} of {1} after {2:.3f} seconds".format(i, attempts + 1, duration),)

    raise
