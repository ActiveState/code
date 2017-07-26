## Emacs-like hotkey support for wxPython

Originally published: 2005-11-21 22:45:31
Last updated: 2005-11-22 06:50:06
Author: Josiah Carlson

Some people have a burning need for emacs-like multiple key sequence hotkeys.  What do I mean?  Ctrl+x Ctrl+s to save the currently open document and exit emacs.\n\nIncluded as code is a sample wxPython program which implements multi-group keypress combinations, and will print 'hello!' in the statusbar if the combination Ctrl+Y Alt+3 Shift+B is entered.  As you are entering a valid sequence of hotkeys, it will print your current combination in the status bar.  If you make a mistake, it will print out your failed keyboard combination.\n\nI use variants of the menu manupulation and keymap generation code in PyPE (http://pype.sf.net).