def identity(x):
    return x

def foldsh(tree, branch= lambda tree,ch: list(ch), leaf=identity, shared=identity, getchildren=iter):
    '''Sharing-aware tree transformations.
    
    foldsh(tree,branch,leaf,shared,getchildren) :: tree -> result
    
    branch      :: tree, list of children's results -> result
    leaf        :: tree -> result
    shared      :: result -> result
    getchildren :: tree -> iterable of children'''
    
    mem = dict()
    def _fold(tree):
        if id(tree) in mem:
            return shared(mem[id(tree)])
        else:
            try:
                children = getchildren(tree)
            except:
                res = leaf(tree)
            else:
                reschildren = [_fold(child) for child in children]
                res = branch(tree,reschildren)
            mem[id(tree)] = res
            return res
    return _fold(tree)
