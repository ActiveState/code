from difflib import get_close_matches # for __getattr__

class Demo(object):
    def __getattr__(self, name):
        """If a wrong method is called, this suggests methods with similar names."""
        toRemove = """__delattr__ __dict__ __getattribute__ __module__ __new__
                      __reduce__ __copy__ __reduce_ex__ __setattr__ __slot__
                      __weakref__ __str__ __class__ __doc__""".split()
        methods = set(dir(self.__class__)).difference(toRemove)
        suggestions = get_close_matches(name.lower(), methods, 5)
        raise_comment = "method '%s' not found.\n" % name
        raise_comment += "Most similar named ones: %s\n\n" % ", ".join(suggestions)
        first_lines = []
        for method in suggestions:
            doc = getattr(self.__class__, method).__doc__
            if doc:
                first_lines.append(doc.splitlines()[0])
            else:
                first_lines.append(method + " - no docstring found.")
        raise AttributeError, raise_comment + "\n".join(first_lines)

    # Some useless methods for this demo
    def addcube(self):
        """docstring of addcube()"""
    def addrube(self):
        """docstring of addrube()"""
    def adder(self):
        """docstring of adder()"""
    def waiter(self):
        """docstring of waiter()"""
    def boiler(self):
        """docstring of boiler()"""

# Test of the __getattr__
d = Demo()
d.addCube()
