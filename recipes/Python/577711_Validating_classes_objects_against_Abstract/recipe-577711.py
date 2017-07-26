def validate(obj, classes=None):
    """
    Validate the object against the classes.

    This is like isinstance, except that it validates that the object 
    has implemented all the abstract methods/properties of all the 
    classes.

    """
    if classes is None:
        classes = obj.mro()
        #classes.extend(obj.__implements__)
    if not isinstance(classes, (list, tuple)):
        classes = (classes,)
    abstracts = set()
    for cls in classes:
        if not isinstance(cls, type):
            raise TypeError("Can only validate against classes")
        for name in getattr(cls, "__abstractmethods__", set()):
            value = getattr(obj, name, None)
            if not value:
                abstracts.add(name)
            elif getattr(value, "__isabstractmethod__", False):
                abstracts.add(name)
    if abstracts:
        sorted_methods = sorted(abstracts)
        joined = ", ".join(sorted_methods)
        try:
            name = obj.__name__
        except AttributeError:
            name = obj
        msg = "{} does not implement abstract methods {}"
        raise TypeError(msg.format(name, joined))


def conforms(classes):
    """A class decorator factory for validating against an ABC."""
    def decorator(cls):
        if not __debug__:
            return cls
        if not isinstance(cls, type):
            raise TypeError("Can only validate classes")
        validate(cls, classes)
        return cls
    return decorator
