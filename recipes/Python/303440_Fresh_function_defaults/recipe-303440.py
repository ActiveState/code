from copy import deepcopy

def freshdefaults(f):
    "wrap f and keep its default values fresh between calls"
    fdefaults = f.func_defaults
    def refresher(*args, **kwds):
        f.func_defaults = deepcopy(fdefaults)
        return f(*args, **kwds)
    return refresher

# usage, python 2.4+
@freshdefaults
def packitem(item, pkg=[]):
    pkg.append(item)
    return pkg

# for older python versions, 
# use f = freshdefaults(f)
