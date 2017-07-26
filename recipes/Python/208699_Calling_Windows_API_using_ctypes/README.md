## Calling Windows API using ctypes and win32con  
Originally published: 2003-07-03 13:08:14  
Last updated: 2008-07-25 20:01:50  
Author: Gary Eakins  
  
It is easy to call Windows API dlls using the
ctypes module with win32con defining the
constant values for message identifiers and
parameter flags. The demo code shows a simple
but complete application that registers a
window class and a Python WndProc callback function,
creates the window and pumps messages.