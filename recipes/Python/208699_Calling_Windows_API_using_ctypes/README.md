## Calling Windows API using ctypes and win32con

Originally published: 2003-07-03 13:08:14
Last updated: 2008-07-25 20:01:50
Author: Gary Eakins

It is easy to call Windows API dlls using the\nctypes module with win32con defining the\nconstant values for message identifiers and\nparameter flags. The demo code shows a simple\nbut complete application that registers a\nwindow class and a Python WndProc callback function,\ncreates the window and pumps messages.