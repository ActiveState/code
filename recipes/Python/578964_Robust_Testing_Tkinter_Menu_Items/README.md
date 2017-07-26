## Robust Testing of Tkinter Menu Items with Mocking.

Originally published: 2014-11-16 20:48:28
Last updated: 2016-07-27 10:52:09
Author: Stephen Rigden

This recipe addresses the problems encountered when building robust tests for Tk menus.\nThe software under test is a simple window with two menu items that each invoke a one button dialog box. All user visible text is imported from an external config.ini file.\nThis scenario can lead to fragile test code because of the way TK's invoke(index) command has been implemented. (Tcl8.6.3/Tk8.6.3.)