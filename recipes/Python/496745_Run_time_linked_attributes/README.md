## Run time linked attributes  
Originally published: 2006-05-28 15:00:16  
Last updated: 2006-05-28 15:00:16  
Author: Michael Murr  
  
A metaclass that allows the runtime creation of parent references, without needing to pass them on the command line.  For example:

a.b -> (points to) b
b.creator -> (points to) a