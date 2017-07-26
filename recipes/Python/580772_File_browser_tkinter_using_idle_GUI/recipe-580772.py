try:
    from Tkinter import Tk
except ImportError:
    from tkinter import Tk

from idlelib.TreeWidget import ScrolledCanvas, FileTreeItem, TreeNode
import os

root = Tk()
root.title("Test TreeWidget")

sc = ScrolledCanvas(root, bg="white", highlightthickness=0, takefocus=1)
sc.frame.pack(expand=1, fill="both", side="left")

item = FileTreeItem(os.getcwd())
node = TreeNode(sc.canvas, None, item)
node.expand()

root.mainloop()
