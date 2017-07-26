import sys
import types

visited = set()

def tree(parent, mod, indent = 0):
    print '"%s" -> "%s" ; '%(parent, mod.__name__)
    if mod in visited:
        return
    visited.add(mod)
    for i in dir(mod):
        obj = getattr(mod, i)
        if isinstance(obj, types.ModuleType):
            tree(mod.__name__, obj, indent + 1)

if __name__ == "__main__":
    class Foo: pass
    Foo.__name__ = "Top"
    mod = __import__(sys.argv[1])
    print "Digraph F {"
    tree(Foo, mod)
    print "}"
