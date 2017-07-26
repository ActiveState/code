def __init__(self):
    """Loop on all base classes, and invoke their constructors.
    Protect against diamond inheritance."""
    for base in self.__class__.__bases__:
        # Avoid problems with diamond inheritance.
        basekey = 'init_' + str(base)
        if not hassattr(self, basekey):
            setattr(self, basekey, 1)
        else:
            continue
        # Call this base class' constructor if it has one.
        if hasattr(base, "__init__"):
            base.__init__(self)

def __del__(self):
    """Loop on all base classes, and invoke their destructors.
    Protect against diamond inheritance."""
    for base in self.__class__.__bases__:
        # Avoid problems with diamond inheritance.
        basekey = 'del_' + str(base)
        if not hasattr(self, basekey):
            setattr(self, basekey, 1)
        else:
            continue
        # Call this base class' destructor if it has one.
        if hasattr(base, "__del__"):
            base.__del__(self)
