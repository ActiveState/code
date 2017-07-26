"""freeze module

The freeze and unfreeze functions special-case some of the built-in
types.  If these types grow the appropriate methods then that will
become unnecessary.

"""

__all__ = ("Freezable", "UnFreezable", "freeze", "unfreeze")


import builtins
from abc import ABCMeta, abstractmethod


class Freezable(metaclass=ABCMeta):

    @abstractmethod
    def __freeze__(self):
        """Returns an immutable version of this object."""


class UnFreezable(metaclass=ABCMeta):

    @abstractmethod
    def __unfreeze__(self):
        """Returns a mutable version of this object."""


def freeze(obj):
    """Returns the immutable version of the object."""

    if hasattr(type(obj), "__freeze__"):
        return obj.__freeze__()
    try:
        handler = _freeze_registry[type(obj)]
    except KeyError:
        pass
    else:
        return handler(obj)
    #if hasattr(type(obj), "__unfreeze__"):
    #    return obj

    msg = "Don't know how to freeze a {} object"
    raise TypeError(msg.format(type(obj)))


def unfreeze(obj, strict=False):
    if hasattr(type(obj), "__unfreeze__"):
        return obj.__unfreeze__()
    try:
        handler = _unfreeze_registry[type(obj)]
    except KeyError:
        pass
    else:
        return handler(obj)
    #if hasattr(type(obj), "__freeze__"):
    #    return obj

    msg = "Don't know how to unfreeze a {} object"
    raise TypeError(msg.format(type(obj)))


#################################################
# special-casing built-in types

_freeze_registry = {}
_unfreeze_registry = {}
def register(f, cls=None):
    action, typename = f.__name__.split("_")
    if cls is None:
        cls = getattr(builtins, typename)
    if action == "freeze":
        _freeze_registry[cls] = f
        Freezable.register(cls)
    elif action == "unfreeze":
        _unfreeze_registry[cls] = f
        UnFreezable.register(cls)
    else:
        raise TypeError
    return f


@register
def freeze_dict(obj):
    raise NotImplementedError

@register
def unfreeze_dict(obj):
    return obj


@register
def freeze_list(obj):
    return tuple(obj)

@register
def unfreeze_list(obj):
    return obj


@register
def freeze_tuple(obj):
    return obj

@register
def unfreeze_tuple(obj):
    return list(obj)
