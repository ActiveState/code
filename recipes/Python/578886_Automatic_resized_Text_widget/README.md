## Automatic resized Text widget (Tkinter)  
Originally published: 2014-06-04 18:53:33  
Last updated: 2016-12-10 15:40:25  
Author: Miguel Martínez López  
  
The Text widget resize to its contents.
Based on this:
https://stackoverflow.com/questions/11544187/tkinter-resize-text-to-contents

But here there is one important improvement:
The widget resize first, before a character inclusion.

For this trick I have had to use tag bindings.

Here there is a practical application of this widget:

https://code.activestate.com/recipes/578885-draggable-desktop-note-or-sticky-notes-in-tkinter/