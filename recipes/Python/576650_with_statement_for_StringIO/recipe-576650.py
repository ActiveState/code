@contextmanager
def StringIO():
    """Add support for 'with' statement to StringIO - http://bugs.python.org/issue1286
    """
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
        
    sio = StringIO()
    
    try:
        yield sio
    finally:
        sio.close()
