"""
author: anton.vredegoor@gmail.com
last edit: Oct 21, 2010

Python directory changer.

This script displays a directory tree. By single clicking on a '+' or '-' sign
one can expand/collapse an item. Double clicking on an item itself, 
if that item is a directory, results in the script printing its location to 
standard output, and then exiting.

The idea is to create a script to start a graphical directory browser
from a terminal window and switch the terminal it is started from 
to the new directory.

Since a script cannot change the environment of its parent we need a
little trick to make this work.

Create an alias (for example in .bashrc or in .bash_aliases) like this:

alias pycd='python ~/pycd.py > ~/pycd.out && . ~/pycd.out'

(This alias expects pycd.py to be in the user's home directory,  so put 
it there or adapt the alias)

Now typing 'pycd' in a terminal (without the quotes) opens the browser
and redirects the script's output to the file 'pycd.out', and then (after the 
script has exited) executes the cd command in that file, in the shell. 

The result is, we end up in the desired directory.

The script needs the TreeWidget from idle, so one should
install idle:

sudo aptitude install idle

(or equivalent)

If necessary, adjust the sys.path.append line, to make it point 
to your idlelib location.

"""

import sys
import os
from string import replace
from Tkinter import *

sys.path.append(r'/usr/lib/python2.6/idlelib')

from TreeWidget import FileTreeItem, TreeNode, ScrolledCanvas

class MyFileTreeItem(FileTreeItem):
    
    def GetSubList(self):
        try:
            names = os.listdir(self.path)
        except os.error:
            return []
        names.sort(lambda a, b: cmp(os.path.normcase(a).lower(), os.path.normcase(b).lower()))
        sublist = []
        for name in names:
            item = MyFileTreeItem(os.path.join(self.path, name))
            sublist.append(item)
        return sublist

    def OnDoubleClick(self):
        if self.IsExpandable():
            sys.stdout.write('cd %s' %(replace(self.path,' ','\ ')))
            sys.exit()

def test():
    root = Tk()
    sys.exitfunc = root.quit
    root.configure(bd=0, bg="yellow")
    root.title("terminal directory changer")
    root.focus_set()
    sc = ScrolledCanvas(root, bg="white", highlightthickness=0, takefocus=1)
    sc.frame.pack(expand=1, fill="both")
    item = MyFileTreeItem('/')
    node = TreeNode(sc.canvas, None, item)
    node.expand()
    root.mainloop()

if __name__=='__main__':
    test()
