## SuperText - Scrollable text with pop-up menu and themes for Tkinter  
Originally published: 2014-06-20 16:23:35  
Last updated: 2014-06-20 16:25:43  
Author: Peter Mojeiko  
  
Two things I consistently need when using a Text widget are scrollbars and pop-up menus. I've been adding them in on the fly for a while, but I think this class provides an easier way to implement these features.

I also added a couple of very minimal themes:

    1. The terminal theme replaces the standard Text cursor with a blocky-style
    insert cursor

    2. The typewriter theme takes any text that has been inserted before it is called
    and types it to the widget, one character at a time

There's an example of use at the bottom of the code.