class fake_module(object):
    def __init__(self, name, *args):
        self.name = name
        self.__all__ = []
        for func in args:
            name = func.__name__
            self.__dict__[name] = func
            self.__all__.append(name)
    def register(self):
        sys.modules["%s.%s" % (__name__, self.name)] = self

fake_module('api', class1, class2, func3, exception4).register()
