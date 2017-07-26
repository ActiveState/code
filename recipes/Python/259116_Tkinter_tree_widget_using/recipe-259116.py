# domtree.py
# This is a simple example for idlelib.TreeWidget

# Written by Seo Sanghyeon
# Put into the public domain

from Tkinter import Tk, Canvas
from xml.dom.minidom import parseString
from idlelib.TreeWidget import TreeItem, TreeNode

class DomTreeItem(TreeItem):
    def __init__(self, node):
        self.node = node
    def GetText(self):
        node = self.node
        if node.nodeType == node.ELEMENT_NODE:
            return node.nodeName
        elif node.nodeType == node.TEXT_NODE:
            return node.nodeValue
    def IsExpandable(self):
        node = self.node
        return node.hasChildNodes()
    def GetSubList(self):
        parent = self.node
        children = parent.childNodes
        prelist = [DomTreeItem(node) for node in children]
        itemlist = [item for item in prelist if item.GetText().strip()]
        return itemlist

data = '''
<a>
 <b>
  <c>d</c>
  <c>e</c>
 </b>
 <b>
  <c>f</c>
 </b>
</a>
'''

root = Tk()
canvas = Canvas(root)
canvas.config(bg='white')
canvas.pack()
dom = parseString(data)
item = DomTreeItem(dom.documentElement)
node = TreeNode(canvas, None, item)
node.update()
node.expand()
root.mainloop()
