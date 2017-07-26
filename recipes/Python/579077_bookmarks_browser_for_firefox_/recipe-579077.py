import sys
from argparse import ArgumentParser
from Tkinter import *
sys.path.append(r'/usr/lib/python2.7/idlelib')
from TreeWidget import FileTreeItem, TreeNode, ScrolledCanvas

class MyFileTreeItem(FileTreeItem):

    def GetText(self):
            return self.path.get("title")

    def SetText(self, text):
        pass
        
    def GetSubList(self):
        return [MyFileTreeItem(name) for name in self.path['children']]
        
    def IsExpandable(self):
        """Return whether there are subitems."""
        return self.path.has_key('children')
 
    def IsEditable(self):
        pass
               
    def OnDoubleClick(self):
        if not self.IsExpandable():
            print self.path.get('uri','no uri available')

def main():
    parser = ArgumentParser(description = 'browse a bookmarks_xxx.json file')
    parser.add_argument('jbfile', 
        help='the json file containing the bookmarks')
    args = parser.parse_args()
    root = Tk()
    sys.exitfunc = root.quit
    root.configure(bd=0, bg="yellow")
    root.title("bookmarks browser")
    root.focus_set()
    sc = ScrolledCanvas(root, bg="white", highlightthickness=0, takefocus=1)
    sc.frame.pack(expand=1, fill="both")
    fn =args.jbfile
    D = eval(file(fn).read())
    D['title'] = fn
    item = MyFileTreeItem(D)
    node = TreeNode(sc.canvas, None, item)
    node.expand()
    root.mainloop()

if __name__=='__main__':
    main()
