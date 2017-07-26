## Elisp code to insert super calls in Emacs  
Originally published: 2007-06-24 11:49:28  
Last updated: 2007-06-24 11:49:28  
Author: Carl Banks  
  
This elisp code creates a key binding which inserts a new-style call to the base class method (using super) with the appropriate class and method name.  For instance, if the point is inside method __init__ in class Widget, typing C-c C-f will insert the text "super(Widget,self).__init__()".\n\nRequires Emacs and python-mode.el.