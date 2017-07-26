import abc

class ABCMeta(abc.ABCMeta):
    def register(cls, subclass):
        subclass = super(ABCMeta, cls).register(subclass)
        if not hasattr(subclass, "__implements__"):
            try:
                subclass.__implements__ = {cls}
            except TypeError:
                pass
        else:
            subclass.__implements__.add(cls)
        return subclass
