import sys, pickle

def makeFakeClass(module, name):
    class FakeThing(object): 
        pass
    FakeThing.__name__ = name
    FakeThing.__module__ = '(fake)' + module
    return FakeThing

class PickleUpgrader(pickle.Unpickler):
    def find_class(self, module, cname):
        # Pickle tries to load a couple things like copy_reg and
        # __builtin__.object even though a pickle file doesn't
        # explicitly reference them (afaict): allow them to be loaded
        # normally.
        if module in ('copy_reg', '__builtin__'):
            thing = pickle.Unpickler.find_class(self, module, cname)
            return thing
        return makeFakeClass(module, cname)

root = PickleUpgrader(open(sys.argv[1])).load()

# Do whatever to 'root' here.
