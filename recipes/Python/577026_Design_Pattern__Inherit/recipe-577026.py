def MakeClassFromInstance(instance):
    from copy import deepcopy
    copy = deepcopy(instance.__dict__)
    InstanceFactory = type('InstanceFactory', (instance.__class__, ), {})
    InstanceFactory.__init__ = lambda self, *args, **kwargs: self.__dict__.update(copy)
    return InstanceFactory
