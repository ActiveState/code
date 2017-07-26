## Flexible Win32 message pump using MsgWaitForMultipleObjects  
Originally published: 2001-10-17 14:54:27  
Last updated: 2002-06-06 16:07:11  
Author: Michael Robin  
  
In win32, as in other event-driven systems, you must process messages or bad things happen.\n(Or at best, good things don't happen.) The MsgWaitForMultipleObjects is one way to deal\nwith handling messages as well as coordinating several other activities.