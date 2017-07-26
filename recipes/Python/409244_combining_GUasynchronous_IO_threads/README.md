## combining GUIs and asynchronous I/O with threads and pygtk  
Originally published: 2005-04-10 08:36:58  
Last updated: 2005-04-10 08:36:58  
Author: Pierrre Amadio  
  
You need to access socket, serial ports, or other asynchronous but blocking I/O sources while running a GUI with pygtk.

The cookbook already gives example suited for Tkinker and PyQt.

Here is an attempt to do the same with pygtk based on the Tkinker and PyQt example.