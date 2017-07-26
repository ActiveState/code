import itertools as _itertools

class Amb(object):
    def __init__(self):
        self._names2values   = {}       # set of values for each global name
        self._func           = None     # Boolean constraint function
        self._valueiterator  = None     # itertools.product of names values
        self._funcargnames   = None     # Constraint parameter names

    def __call__(self, arg=None):
        if hasattr(arg, 'func_globals'):
            ##
            ## Called with a constraint function. 
            ##
            globls = arg.func_globals
            # Names used in constraint
            argv = arg.__code__.co_varnames[:arg.__code__.co_argcount]
            for name in argv:
                if name not in self._names2values:
                    assert name in globls, \
                           "Global name %s not found in function globals" % name
                    self._names2values[name] = globls[name]
            # Gather the range of values of all names used in the constraint
            valuesets = [self._names2values[name] for name in argv]
            self._valueiterator = _itertools.product(*valuesets)
            self._func = arg
            self._funcargnames = argv
            return self
        elif arg is not None:
            ##
            ## Assume called with an iterable set of values
            ##
            arg = frozenset(arg)
            return arg
        else:
            ##
            ## blank call tries to return next solution
            ##
            return self._nextinsearch()

    def _nextinsearch(self):
        arg = self._func
        globls = arg.func_globals
        argv = self._funcargnames
        found = False
        for values in self._valueiterator:
            if arg(*values):
                # Set globals.
                found = True
                for n, v in zip(argv, values):
                    globls[n] = v
                break
        if not found: raise StopIteration
        return values

    def __iter__(self):
        return self
    
    def next(self):
        return self()

if __name__ == '__main__':
    if True:
        amb = Amb()
        
        print("\nSmall Pythagorean triples problem:")
        x = amb(range(1,11))
        y = amb(range(1,11))
        z = amb(range(1,11))

        for _dummy in amb( lambda x, y, z: x*x + y*y == z*z ):
            print x, y, z


    if True:
        amb = Amb()
        
        print("\nRosetta Code Amb problem:")
        w1 = amb(["the", "that", "a"])
        w2 = amb(["frog", "elephant", "thing"])
        w3 = amb(["walked", "treaded", "grows"])
        w4 = amb(["slowly", "quickly"])

        for _dummy in amb( lambda w1, w2, w3, w4: \
                             w1[-1] == w2[0] and \
                             w2[-1] == w3[0] and \
                             w3[-1] == w4[0] ):
            print w1, w2, w3, w4

    if True:
        amb = Amb()
        
        print("\nAmb problem from "
            "http://www.randomhacks.net/articles/2005/10/11/amb-operator:")
        x = amb([1, 2, 3])
        y = amb([4, 5, 6])

        for _dummy in amb( lambda x, y: x * y != 8 ):
            print x, y
