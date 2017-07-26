## Transparent HTTP Tunnel for Python sockets (to be used by ftplib )  
Originally published: 2011-04-07 13:26:27  
Last updated: 2011-11-07 10:25:56  
Author: Raphaël Jolivet  
  
This script allows how to transparently install a HTTP proxy (proxy HTTP 1.1, using CONNECT command) on all outgoing sockets.

I did that to bring TCP over HTTP to FTPlib, transparently.
It should enable HTTP tunneling for all methods / modules that use the low-level socket API.
