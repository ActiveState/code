"""mixin module

"""

def add_mixin(cls, mixin, force=False):
    """Add the public attributes of a mixin to another class.

    Attribute name collisions result in a TypeError if force is False.
    If a mixin is an ABC, the decorated class is registered to it,
    indicating that the class implements the mixin's interface.

    """

    for name, value in mixin.__dict__.items():
        if name.startswith("_"):
            continue
        if not force and hasattr(cls, name):
            raise TypeError("name collision ({})".format(name))
        setattr(cls, name, value)
    try:
        mixin.register(cls)
    except AttributeError:
        pass
    

def mixes_in(*mixins, force=False):
    """A class decorator factory that adds mixins using add_mixin.

    """

    def decorator(cls):
        for mixin in mixins:
            add_mixin(cls, mixin, force)
        return cls
    return decorator
