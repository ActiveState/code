import sys


if sys.version_info[0:2] < (3, 5):
    raise ValueError('Python >=3.5 is required!')


# Example usage:

# from auto_assign import *
# class Xyz:
#     @auto_assign
#     def __init__(self, x: AutoAssign[int]) -> None:
#         pass

# xyz = Xyz(1)
# print(xyz.x)  # 1

# (See the description for more details...)


from typing import Any, Callable, TypeVar, Union, cast
import inspect


class _AutoAssignMagic: pass
_T = TypeVar('_T')
AutoAssign = Union[_AutoAssignMagic, _T]


_F = TypeVar('_F', bound=Callable[..., Any])


def auto_assign(func: _F) -> _F:
    def _wrap(*args, **kw):
        if not args:
            # Where is self? Let the function figure it out!
            func(*args, **kw)

        self = args[0]

        sig = inspect.signature(func)
        auto_args = set()

        for param in sig.parameters.values():
            # XXX: Hacky way of checking for AutoAssign.
            if hasattr(param.annotation, '__origin__') and \
               param.annotation.__origin__ is AutoAssign:
                auto_args.add(param.name)

        try:
            bound = sig.bind(*args, **kw)
        except TypeError:
            # Just let it propagate down to the function itself.
            pass
        else:
            bound.apply_defaults()
            for auto_arg in auto_args:
                setattr(self, auto_arg, bound.arguments[auto_arg])

        func(*args, **kw)

    return cast(_F, _wrap)
