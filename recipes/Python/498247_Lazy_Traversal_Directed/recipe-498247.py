def graphWalker(node, getChildren, toEvaluate, backPack = None):
    """
    A generator that (lazily, recursively) applies an operation to a directed graph structure.
    
    @param node the graph node where we start
    @param getChildren a callable f such that f(node) returns the child nodes of node
    @param toEvaluate a callable g such that the result rr for a node is rr = g(node, backPack)[0]
    @param backPack a partial result that is carried along and may change as the graph is traversed. 
            g(node, backPack)[1] is passed on to the child nodes.
    @returns an iterator over the results of applying toEvaluate to every node in the tree
    
    @see walkTest() for an example.
    """
    rr = toEvaluate(node, backPack)
    yield rr[0]
    for child in getChildren(node):
        for result in graphWalker(child, getChildren, toEvaluate, rr[1]):
            yield result



"""

SAMPLE (TEST) CODE FOLLOWS:

"""

import os
import stat
       
def walkTest(root = os.getcwd(), recursionLimit = 3):
    """
    A walk that prints all the relative path of all files in a file system rooted 
    at the current directory with respect to that directory. Goes no deeper than
    recursionLimit.
    """
    
    def te(node, rl):
        root, visitedNodes, name = node[:3]
        if rl < 0: raise StopIteration
        return (
                os.sep.join(visitedNodes + [name])[1:],
                rl - 1
                )
    
    def absPath(node):
        return os.sep.join(
                               [node[0]] + node[1] + [node[2]]
                               )
    
    def isdir(path):
        """
        @param path the absolute (?) path of the file
        """
        return stat.S_ISDIR(os.stat(
                                    path
                                    )[stat.ST_MODE])
        
    def gc(node):
        
        root, visitedNodes, name, depth = node
        
        ab = absPath(node)
        if not isdir(ab): return []
        

        return [
                (
                 root,
                 visitedNodes + [name],
                 cc,
                 depth + 1
                 )
                for cc in
                os.listdir(ab)]

    return graphWalker((root, [], "", 0), gc, te, recursionLimit)

if __name__ == "__main__":
    for rr in walkTest():
        print rr
    
