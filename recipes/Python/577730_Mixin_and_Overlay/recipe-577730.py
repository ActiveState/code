from collections.abc import ABCMeta, abstractmethod


class MixinError(TypeError): pass

class MixinMeta(type):
    """Build classes that easily mix in to other classes."""
    def __new__(self, name, bases, namespace):
        cls = super(MixinMeta, self).__new__(self, name, bases, namespace)
        if "__mixins__" not in namespace:
            cls.__mixins__ = tuple(name for name in namespace if name != "__module__")
        return cls

    def mixes_in(cls, target):
        """Class decorator to add the __mixins__ of cls into target.
        
        If any mixin attribute's name is already bound on the target,
        raise a MixinError.

        The target is returned, modified.

        """

        # check for all mixin attrs before adding
        for attr in cls.__mixins__:
            if hasattr(target, attr):
                raise MixinError("Attribute already exists: %s" % attr)
        for attr in cls.__mixins__:
            setattr(target, attr, getattr(cls, attr))
        return cls.register(target)


class OverlayError(TypeError): pass

class OverlayMeta(type):
    """Build classes that easily wrap the methods of other classes."""
    def __new__(self, name, bases, namespace):
        cls = super(OverlayMeta, self).__new__(self, name, bases, namespace)
        cls.__overlays__ = tuple(name for name in namespace if name != "__module__")
        return cls

    def overlays(cls, target):
        """Class decorator to wrap the target's methods.

        If any overlay attribute's name is not bound on the target,
        raise an OverlayError.

        The target is used as the base class for a new class, which is
        returned.

        """

        # check for all overlay attrs before adding
        for attr in cls.__overlays__:
            if not hasattr(target, attr):
                raise OverlayError("Expected attribute: %s" % attr)
        class Temp(target):
            __doc__ = target.__doc__
            for attr in cls.__overlays__:
                locals()[attr] = getattr(cls, attr)
            del attr
        Temp.__name__ = target.__name__
        return Temp
