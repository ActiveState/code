def printBfsLevels(graph,start):
  queue=[start]
  path=[]
  currLevel=1
  levelMembers=1
  height=[(0,start)]
  childCount=0
  print queue
  while queue:
    visNode=queue.pop(0)
    if visNode not in path:
      if  levelMembers==0:
        levelMembers=childCount
        childCount=0
        currLevel=currLevel+1
      queue=queue+graph.get(visNode,[])
      if levelMembers > 0:
        levelMembers=levelMembers-1
        for node in graph.get(visNode,[]):
          childCount=childCount+1
          height.append((currLevel,node))
      path=path+[visNode]

  prevLevel=None
  
  for v,k in sorted(height):
        if prevLevel!=v:
          if prevLevel!=None:
            print "\n"
        prevLevel=v
        print k,
  return height

g={1: [2, 3,6], 2: [4, 5], 3: [6, 7],4:[8,9,13]}
printBfsLevels(g,1)


>>> 
[1]
1 

2 3 6 

4 5 6 7 

8 9 13
>>> 

# Another version based on Recursion, Which is specific to Binary tree


class BinTree:
  "Node in a binary tree"
  def __init__(self,val,leftChild=None,rightChild=None,root=None):
    self.val=val
    self.leftChild=leftChild
    self.rightChild=rightChild
    self.root=root
    if not leftChild and not rightChild:
      self.isExternal=True

  def getChildren(self,node):
    children=[]
    if node.isExternal:
      return []
    if node.leftChild:
      children.append(node.leftChild)
    if node.rightChild:
      children.append(node.rightChild)
    return children

  @staticmethod
  def createTree(tupleList):
    "Creates a Binary tree Object from a given Tuple List"
    Nodes={}
    root=None
    for item in treeRep:
      if not root:
        root=BinTree(item[0])
        root.isExternal=False
        Nodes[item[0]]=root
        root.root=root
        root.leftChild=BinTree(item[1],root=root)
        Nodes[item[1]]=root.leftChild
        root.rightChild=BinTree(item[2],root=root)
        Nodes[item[2]]=root.rightChild
      else:
        CurrentParent=Nodes[item[0]]
        CurrentParent.isExternal=False
        CurrentParent.leftChild=BinTree(item[1],root=root)
        Nodes[item[1]]=CurrentParent.leftChild
        CurrentParent.rightChild=BinTree(item[2],root=root)
        Nodes[item[2]]=CurrentParent.rightChild
    root.nodeDict=Nodes
    return root

  def printBfsLevels(self,levels=None):
    if levels==None:
      levels=[self]
    nextLevel=[]
    for node in levels:
      print node.val,
    for node in levels:
      nextLevel.extend(node.getChildren(node))
    print '\n'
    if nextLevel:
      node.printBfsLevels(nextLevel)  
     

##       1
##     2     3
##   4   5  6  7
##  8

treeRep = [(1,2,3),(2,4,5),(3,6,7),(4,8,None)]
tree= BinTree.createTree(treeRep)
tree.printBfsLevels()

>>> 
1 

2 3 

4 5 6 7 

8 None 
