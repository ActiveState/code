import threading
from contextlib import contextmanager

_tls = threading.local()

@contextmanager
def _nested():
    _tls.level = getattr(_tls, "level", 0) + 1
    try:
        yield "   " * _tls.level
    finally:
        _tls.level -= 1

@contextmanager
def _recursion_lock(obj):
    if not hasattr(_tls, "history"):
        _tls.history = []  # can't use set(), not all objects are hashable
    if obj in _tls.history:
        yield True
        return
    _tls.history.append(obj)
    try:
        yield False
    finally:
        _tls.history.pop(-1)

def humanize(cls):
    def __repr__(self):
        if getattr(_tls, "level", 0) > 0:
            return str(self)
        else:
            attrs = ", ".join("%s = %r" % (k, v) for k, v in self.__dict__.items())
            return "%s(%s)" % (self.__class__.__name__, attrs)

    def __str__(self):
        with _recursion_lock(self) as locked:
            if locked:
                return "<...>"
            with _nested() as indent:
                attrs = []
                for k, v in self.__dict__.items():
                    if k.startswith("_"):
                        continue
                    if isinstance(v, (list, tuple)) and v:
                        attrs.append("%s%s = [" % (indent, k))
                        with _nested() as indent2:
                            for item in v:
                                attrs.append("%s%r," % (indent2, item))
                        attrs.append("%s]" % (indent,))
                    elif isinstance(v, dict) and v:
                        attrs.append("%s%s = {" % (indent, k))
                        with _nested() as indent2:
                            for k2, v2 in v.items():
                                attrs.append("%s%r: %r," % (indent2, k2, v2))
                        attrs.append("%s}" % (indent,))
                    else:
                        attrs.append("%s%s = %r" % (indent, k, v))
                if not attrs:
                    return "%s()" % (self.__class__.__name__,)
                else:
                    return "%s:\n%s" % (self.__class__.__name__, "\n".join(attrs))

    cls.__repr__ = __repr__
    cls.__str__ = __str__
    return cls
