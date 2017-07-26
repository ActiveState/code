## Extending socket.socketpair() to work on WindowsOriginally published: 2007-07-22 22:36:21 
Last updated: 2007-07-22 22:36:21 
Author: Bob Ziuchkovski 
 
This recipe wraps socketpair() to provide a standard socket pair on POSIX systems or a pair of connected sockets using ephemeral ports on Windows.