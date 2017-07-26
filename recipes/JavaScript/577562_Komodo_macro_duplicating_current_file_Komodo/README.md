## A Komodo macro for duplicating the current file in Komodo 6Originally published: 2011-02-03 23:47:40 
Last updated: 2011-02-03 23:47:41 
Author: Eric Promislow 
 
The project/file API changed significantly moving from Komodo 5 to 6.\nSpecifically, the project manager and file manager have been split into\ntwo separate modules.\n\nHere's some code to duplicate the current file, using Komodo 6.\nNote that it uses an internal function - I've made a note that the function\nhas been effectively published, and needs to preserve its current\ninterface.