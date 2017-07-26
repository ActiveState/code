## Inline GIF's with Tkinter  
Originally published: 2001-03-14 17:01:04  
Last updated: 2004-01-30 16:43:32  
Author: Brent Burley  
  
This recipe will let you embed GIF images inside of your source code
for use in Tkinter buttons, labels, etc.  It's really handy for making
toolbars, etc. without worrying about having the right icon files
installed.

The basic technique is to encode the GIF with base64 and store it
as a string literal in the Python code to be passed to Tk PhotoImage.