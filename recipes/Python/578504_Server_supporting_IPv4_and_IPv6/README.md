## Server supporting IPv4 and IPv6  
Originally published: 2013-03-29 01:57:06  
Last updated: 2017-03-05 11:00:27  
Author: Giampaolo Rodolà  
  
Utility functions to create a single server socket which able to listen on both IPv4 and IPv6. Inspired by:
http://bugs.python.org/issue17561

Expected usage:

    >>> sock = create_server_sock(("", 8000))
    >>> if not has_dual_stack(sock):
    ...     sock.close()
    ...     sock = MultipleSocketsListener([("0.0.0.0", 8000), ("::", 8000)])
    >>>

From here on you have a socket which listens on port 8000, all interfaces, serving both IPv4 and IPv6. You can start accepting new connections as usual:

    >>> while True:
    ...     conn, addr = sock.accept()
    ...     # handle new connection

Supports UNIX, Windows, non-blocking sockets and socket timeouts.
Works with Python >= 2.6 and 3.X.