def iterchildren(treectrl, node):
    cid, citem = treectrl.GetFirstChild(node)
    while cid.IsOk(): 
        yield cid
        cid, citem = treectrl.GetNextChild(node, citem)


# sample usage
for i in iterchildren(myTreeControl, someNode):
    print myTreeControl.GetItemText(i)
