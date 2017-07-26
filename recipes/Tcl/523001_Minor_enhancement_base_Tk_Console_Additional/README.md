###Minor enhancement to the base Tk Console. Additional change.

Originally published: 2007-06-27 22:27:48
Last updated: 2007-08-24 01:29:47
Author: Mike Collins

Right click Copy and Paste.\nAnd when you source a script from the command line, you lose the focus, and have to click the mouse button somewhere in the console screen to be able to type again.\nFixed that around line # 616. Inserted "focus $w" and now it works better.