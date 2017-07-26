from contextlib import contextmanager

@contextmanager
def failnow():
    try: 
        yield
    except Exception:
        import sys
        sys.excepthook(*sys.exc_info())
        sys.exit(1)
