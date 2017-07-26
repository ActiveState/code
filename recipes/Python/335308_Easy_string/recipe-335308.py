import sys, UserDict
from string import Template

class Chainmap(UserDict.DictMixin):
    """Combine multiple mappings for sequential lookup. Raymond Hettinger,
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/305268 """

    def __init__(self, *maps):
        self._maps = maps

    def __getitem__(self, key):
        for mapping in self._maps:
            try:
                return mapping[key]
            except KeyError:
                pass
        raise KeyError(key)

def interp(s, dic = None):
    caller = sys._getframe(1)
    if dic:
        m = Chainmap(dic, caller.f_locals, caller.f_globals)
    else:
        m = Chainmap(caller.f_locals, caller.f_globals)
    return Template(s).substitute(m)

## Example:

language="Python"

def printmsg():
    opinion = "favorite"
    print interp("My $opinion language is $language.")
