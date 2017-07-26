## Implementing "Future"s with decorators 
Originally published: 2004-12-05 19:13:08 
Last updated: 2004-12-30 05:26:18 
Author: Justin Shaw 
 
How to kick off a slow process without waiting around for the result.  The process is run in the background until the value is actually needed at which time it blocks until the value is ready.