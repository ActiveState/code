## dal_4.py  
Originally published: 2006-04-26 10:11:38  
Last updated: 2006-04-26 10:11:38  
Author: Stephen Chappell  
  
While DAL3 created and enforced a distinction
among directory blocks, file blocks, and
data blocks (along with providing an easy
interface to directory blocks and files blocks),
DAL4 introduces the concept of linking all of
these blocks together and giving names to
directories and files. While still primitive,
the file system is now unified and allows more
advanced abstractions to be built on top of it.