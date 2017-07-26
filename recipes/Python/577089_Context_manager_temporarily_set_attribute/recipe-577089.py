import contextlib

@contextlib.contextmanager
def temp_setattr(ob, attr, new_value):
    """Temporarily set an attribute on an object for the duration of the
    context manager."""
    replaced = False
    old_value = None
    if hasattr(ob, attr):
        try:
            if attr in ob.__dict__:
                replaced = True
        except AttributeError:
            if attr in ob.__slots__:
                replaced = True
        if replaced:
            old_value = getattr(ob, attr)
    setattr(ob, attr, new_value)
    yield replaced, old_value
    if not replaced:
        delattr(ob, attr)
    else:
        setattr(ob, attr, old_value)
