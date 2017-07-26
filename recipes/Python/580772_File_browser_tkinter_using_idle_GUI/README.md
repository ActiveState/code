## File browser for tkinter using idle GUI library  
Originally published: 2017-04-03 13:19:41  
Last updated: 2017-04-03 13:37:34  
Author: Miguel Martínez López  
  
Idle is installed by default on windows.

For Ubuntu, Linux Mint and Debian run:

      sudo apt-get install idle-python2.7

A tree structure is drawn on a Tkinter Canvas object. A tree item is an object with an icon and a text. The item maybe be expandable and/or editable. A tree item has two kind of icons: A normal icon and an icon when the item is selected. To create the tree structure, it's necessary to create a link between tree items, using a parent-child relationship. 

The canvas is built using a *idlelib.TreeWidget.ScrolledCanvas* class. The *frame* attribute of this object contains a *Frame* Tkinter widget prepared for scrolling. This frame allocates a Tkinter *Canvas* and Tkinter *Scrollbars*. This is the signature:

       ScrolledCanvas(master, **options_for_the_tkinter_canvas)

It accepts exactly the same arguments than a *Canvas* widget.

A tree item should be a subclass of *idlelib.TreeWidget.TreeItem*.

The parent-child relationship between tree items is established using the *idlelib.TreeWidget.TreeNode* class.

This is the signature for **TreeNode(canvas, parent, item)**:

- *canvas* should be a *ScrolledCanvas* instance. 
- *parent* should be the parent item. Leave that to *None* to create a root node.
- *item* should be the child item

*FileTreeItem* is a type of *TreeItem*. The only argument of a file tree item is a path.

Here there is an example of a custom tree item:

https://code.activestate.com/recipes/579077-bookmarks-browser-for-firefox/

To create your own tree items, it's required to subclass *TreeItem*. These are the methods that should be overrided:

- *GetText:* It should return the text string to display.
- *GetLabelText:* It should return label text string to display in front of text (Optional).
- *IsExpandable:* It should return a boolean indicating whether the istem is expandable
- *IsEditable:* It should return a boolean indicating whether the item's text may be edited.
- *SetText:* Get the text to change if the item is is editable
- *GetIconName:* Return name of icon to be displayed normally (Icons should be included in *ICONDIR* directory)
- *GetSelectedIconName:*  Return name of icon to be displayed when selected (Icons should be included in *ICONDIR* directory).
- *GetSubList:* It should return a list of child items (Optional. If not defined, the element is not expandable)
- *OnDoubleClick:* Called on a double-click on the item. (Optional)

Icons should be included in "Icons" subdirectory of path to idlelib library. If you want to use other path, just change *ICONDIR* variable to path to your icons:

     import idlelib
     idlelib.ICONDIR = "Your path to your icons"

Run this to find the path to *idlelib* module:

     python -c "import idlelib; print(idlelib.__file__)"