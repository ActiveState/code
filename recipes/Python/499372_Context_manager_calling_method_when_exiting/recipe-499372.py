from contextlib import contextmanager

@contextmanager
def call_on_exit(obj, call, *args, **kwargs):
    """Get the attribute 'call' from 'obj' and call with the remaining
    arguments upon exiting the context manager.

    Upon entrance 'obj' is returned.

    """
    try:
        yield obj
    finally:
        fxn = getattr(obj, call)
        fxn(*args, **kwargs)
