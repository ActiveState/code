## Building GTK GUIs interactively  
Originally published: 2001-06-08 12:22:01  
Last updated: 2001-09-27 15:49:21  
Author: Brian McErlean  
  
One of pythons greatest strengths is the ability to try things interactively at the interpreter.
Using Tkinter shares this strength, since one can create buttons, windows and other widgets,
and instantly see them onscreen, click on buttons to activate callbacks and still be able to
edit and add to the widgets from the python command line.

While the python GTK bindings are generally excellent, one of their flaws is that this is not possible.
Before anything is actually displayed, the gtk.mainloop() function must be called, ending the
possibility of interactive manipulation.

This recipe is a program which simulates a python interpreter which transparently allows the user to
use gtk widgets without having to call mainloop(), in much the same way as Tk widgets.

This latest version contains enhancements added by Christian Robottom Reis to add readline completion support.