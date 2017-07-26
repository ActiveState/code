import sys
_dir = dir
_sentinel = object()

def dir(obj=_sentinel, glob=None):
    from fnmatch import fnmatchcase
    if obj is _sentinel:
        # Get the locals of the caller, not our locals.
        names = sorted(sys._getframe(1).f_locals)
    else:
        names = _dir(obj)
    if glob is None: return names
    return [name for name in names if fnmatchcase(name, glob)]
