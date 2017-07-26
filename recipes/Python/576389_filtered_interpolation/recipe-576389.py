"""I find this useful when programming, for browsing objects interactively
   like one would do with dir. This module allows one to
   restrict the output from dir to what's required.

   You may find the standard pprint module of use also."""

def dire(o, pat=None):
    """like dir, but can filter results with re pat"""

    names = dir(o)
    if not pat:
        return names

    import re
    pat = re.compile(pat)
    def match(name, fn=pat.search):
       return fn(name) is not None
    return filter(match, names)

def ls(o, pat=None):
    """like dir, but can filter results with glob pat"""

    names = dir(o)
    if not pat:
        return names

    import fnmatch
    def match(name, fn=fnmatch.fnmatch, pat=pat):
       return fn(name, pat)
    return filter(match, names)
