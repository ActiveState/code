def as_class(*bases, metaclass=type, **kwargs):
    def decorator(f):
        namespace = f()
        if "__doc__" not in namespace:
            namespace["__doc__"] = f.__doc__
        return metaclass(f.__name__, bases, namespace)
    return decorator

@as_class(object)
def X():
    def __init__(self, name):
        self.__name__ = name
    def __str__(self):
        return self.__name__
    return locals()

x=X("something")
assert x.__name__ == "something"
print(x)
