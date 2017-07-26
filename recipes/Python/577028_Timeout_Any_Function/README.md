## Timeout Any Function 
Originally published: 2010-02-03 13:33:51 
Last updated: 2010-02-04 17:36:31 
Author: Stephen Chappell 
 
This recipe uses the `multiprocessing` module to kill functions that have run longer than intended. Unlike other recipes that use threading, this code is designed to actually kill execution that has continued for too long. This implementation does not rely on signals or anything that is OS specific, so it should work on any system on which you might need generic timeouts.