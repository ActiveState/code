def multi_getattr(obj, attr, default = None):
    """
    Get a named attribute from an object; multi_getattr(x, 'a.b.c.d') is
    equivalent to x.a.b.c.d. When a default argument is given, it is
    returned when any attribute in the chain doesn't exist; without
    it, an exception is raised when a missing attribute is encountered.

    """
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = getattr(obj, i)
        except AttributeError:
            if default:
                return default
            else:
                raise
    return obj
        
# Example usage
obj  = [1,2,3]
attr = "append.__doc__.capitalize.__doc__"

multi_getattr(obj, attr) #Will return the docstring for the
                         #capitalize method of the builtin string
                         #object
