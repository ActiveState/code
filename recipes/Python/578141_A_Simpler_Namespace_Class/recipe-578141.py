class SimpleNamespace:
    """A simple attribute-based namespace."""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def __repr__(self):
        keys = sorted(k for k in self.__dict__ if not k.startswith('_'))
        content = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
        return "{}({})".format(type(self).__name__, ", ".join(content))


class Namespace(SimpleNamespace):
    def __dir__(self):
        return sorted(k for k in self.__dict__ if not k.startswith('_'))
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    def __ne__(self, other):
        return self.__dict__ != other.__dict__
    def __contains__(self, name):
        return name in self.__dict__
