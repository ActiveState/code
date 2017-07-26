## Threaded Cherry Quixote 
Originally published: 2005-05-26 02:16:32 
Last updated: 2005-09-10 23:41:47 
Author: Jonathan Kolyer 
 
A simple integration of a CherryPy web server, using Quixote template publishing, managed in its own thread.\n\nUsing CherryPy as a web server is a good move because it fixes problems on Windows shutting down a call to serve_forever.  This example extends the CherryPy capability by running it in a seperate thread.  Further extension comes from Quixote, for templating HTML.\n\nOne thing I like about this snippet of code is its simplicity.  And the fact that it solves a large number of design problems, all in one shot.