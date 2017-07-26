## dal_4.py 
Originally published: 2006-04-26 10:11:38 
Last updated: 2006-04-26 10:11:38 
Author: Stephen Chappell 
 
While DAL3 created and enforced a distinction\namong directory blocks, file blocks, and\ndata blocks (along with providing an easy\ninterface to directory blocks and files blocks),\nDAL4 introduces the concept of linking all of\nthese blocks together and giving names to\ndirectories and files. While still primitive,\nthe file system is now unified and allows more\nadvanced abstractions to be built on top of it.