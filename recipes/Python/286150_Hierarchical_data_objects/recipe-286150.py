#!/usr/bin/env python 

class HierarchicalData(object):

    """
        organizes hierarchical data as a tree.
        for convenience inner nodes need not be constructed
        explicitly. see examples below.
    """

    def __init__(self):
        # self._d stores subtrees
        self._d = {}

    def __getattr__(self, name):
        # only attributes not starting with "_" are organinzed
        # in the tree
        if not name.startswith("_"):
            return self._d.setdefault(name, HierarchicalData())
        raise AttributeError("object %r has no attribute %s" % (self, name))

    def __getstate__(self): 
        # for pickling
        return self._d, self._attributes()

    def __setstate__(self, tp):
        # for unpickling
        d,l = tp
        self._d = d
        for name,obj in l: setattr(self, name, obj)

    def _attributes(self):
        # return 'leaves' of the data tree
        return [(s, getattr(self, s)) for s in dir(self) if not s.startswith("_") ]

    def _getLeaves(self, prefix=""):
        # getLeaves tree, starting with self
        # prefix stores name of tree node above
        prefix = prefix and prefix + "."
        rv = {}
        atl = self._d.keys()
        for at in atl:
            ob = getattr(self, at)
            trv = ob._getLeaves(prefix+at)
            rv.update(trv)
        for at, ob in self._attributes():
            rv[prefix+at] = ob
        return rv

    def __str__(self):
        # easy to read string representation of data
        rl = [] 
        for k,v in self._getLeaves().items():
            rl.append("%s = %s" %  (k,v))
        return "\n".join(rl)


def getLeaves(ob, pre=""): 
    """ getLeavess tree, returns dictionary mapping 
        paths from root to leafs to value of leafs 
    """
    return ob._getLeaves(pre)


if __name__=="__main__":
    
    model=HierarchicalData()

    # model.person is contstruted on the fly:
    model.person.surname = "uwe"
    model.person.name = "schmitt"
    model.number = 1

    print 
    print "access via attributes:"
    print
    print "model.person.surname=", model.person.surname
    print "model.person.name=", model.person.name
    print "model.number=", model.number
    print

    print "print complete model:"
    print
    print model
    print 

    import pickle

    o = pickle.loads(pickle.dumps(model))

    print "unpickle after pickle:"
    print
    print o
    print
    print "paths from root to leaves and values at leaves:"
    print 
    print getLeaves(o)
