## Komodo JS Macro - delete marked lines  
Originally published: 2010-08-30 17:32:24  
Last updated: 2010-08-30 17:32:24  
Author: Eric Promislow  
  
You can set bookmarks in Komodo, for ease ni revisiting certain lines. This recipe lets you
delete all the marked lines in the current buffer. This code is undoable, but the markers
are gone for good.  They aren't restored by Scintilla, and having Komodo restore them
would be a pain.