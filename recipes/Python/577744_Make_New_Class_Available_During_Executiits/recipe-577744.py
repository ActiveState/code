"""class_hack module"""

from functools import wraps

class Body:
    def __body__(cls):
        """Generate the class body."""
        return locals()
    
class BodyMeta(type):
    def __new__(meta, name, bases, namespace):
        body = namespace.pop("__body__", None)
        cls = type.__new__(meta, name, bases, namespace)
        if body:
            arg = body.__code__.co_varnames[:body.__code__.co_argcount][0]
            @wraps(body)
            def __body__(cls):
                return dict((k, v) for k, v in body(cls).items() if k != arg)
            for key, value in __body__(cls).items():
                setattr(cls, key, value)

            setattr(cls, "__body__", staticmethod(__body__))
        return cls
