"""show_builtins module"""

import types
import collections
try:
    import builtins
except ImportError:
    builtins = __builtin__

ODict = collections.OrderedDict


def show_builtins():

    keys = ("Warnings", "Exceptions", "Types", "Functions", "Others")
    objs = dict(zip(keys, (ODict() for i in keys)))

    for name in dir(builtins):
        if name in ("__doc__", "__name__", "__package__"):
            continue

        obj = getattr(builtins, name)
        _repr = "<{} object>".format(type(obj).__name__)
        if isinstance(obj, type):
            if issubclass(obj, Warning):
                objs["Warnings"][name] = obj
            elif issubclass(obj, Exception):
                objs["Exceptions"][name] = obj
            else:
                objs["Types"][name] = obj
        elif callable(obj):
            if isinstance(obj, types.FunctionType):
                objs["Functions"][name] = obj
            else:
                objs["Functions"][name] = _repr
        else:
            objs["Others"][name] = _repr

    for key in keys:
        section_name = " Builtin {}:".format(key)
        print()
        print(section_name)
        print("-"*(len(section_name)+1))
        for name, obj in objs[key].items():
            print("{:<21} {}".format(name, obj))

if __name__ == "__main__":
    show_builtins()
