def identity(x):
    return x
    
def cyclist(tree):
    res = []
    reschildren = yield res
    res.extend(reschildren)
    yield

def foldcyc(tree,branch=cyclist,leaf=identity,shared=identity,getchildren=iter):
    mem = dict()
    def _fold(tree):
        if id(tree) in mem:
            return shared(mem[id(tree)])
        else:
            try:
                children = getchildren(tree)
            except:
                res = leaf(tree)
                mem[id(tree)] = res
                return res
            coroutine = branch(tree)
            res = coroutine.next()
            mem[id(tree)] = res
            reschildren = [_fold(child) for child in children]
            coroutine.send(reschildren)
            return res
    return _fold(tree)
