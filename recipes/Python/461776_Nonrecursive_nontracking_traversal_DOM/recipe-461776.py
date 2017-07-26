def TraverseNode(currentnode, currentdone, currentpath = None, processcallback = None):
    if not currentdone:
        if currentpath != None:
            currentpath.append(currentnode.nodeName)
        # perform whatever action with the currentnode here
        if processcallback:
          processcallback(currentnode)
        firstchild = currentnode.firstChild
        if firstchild != None:
            return (firstchild, False)
        if currentpath != None:
            del currentpath[-1]
    nextsibling = currentnode.nextSibling
    if nextsibling != None:
        return (nextsibling, False)
    parent = node.parentNode
    if (parent != None) and (currentpath != None):
        # as long as parent exists, currentpath is not supposed to be []
        del currentpath[-1]
    return (parent, True)

def TraverseTree(startnode, startpath = []):
    currentnode = startnode
    currentdone = False
    currentpath = startpath
    while startnode != None:
        (currentnode, currentdone) = TraverseNode(currentnode, currentdone, currentpath)
