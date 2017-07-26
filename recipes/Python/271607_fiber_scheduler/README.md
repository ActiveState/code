## fiber scheduler  
Originally published: 2004-03-02 07:21:20  
Last updated: 2008-01-01 15:32:14  
Author: Gertjan   
  
This code is part of HTTP Replicator (http://sourceforge.net/projects/http-replicator), a proxy server that replicates remote directory structures. The fiber module is an I/O scheduler similar to python's built-in asyncore framework, but based on generators it allows for much more freedom in choosing swich points and wait states.