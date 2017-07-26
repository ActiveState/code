## Reduce memory usage of "re" module 
Originally published: 2005-11-27 07:22:14 
Last updated: 2005-11-27 07:22:14 
Author: Dirk Holtwick 
 
My company wrote an application server that works as a long running service. We were confronted with a memory usage that we couldn't explain until we found out, that the re module is caching a lot of data in the background.