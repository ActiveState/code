###recvall corollary  to socket.sendall

Originally published: 2003-07-30 15:37:35
Last updated: 2003-07-30 15:37:35
Author: John Nielsen

Getting data back from a socket is problematic, because you do no know when it has finished. You'd either need to specify the number of bytes transferred or have some delimeter logic. The function recvall is useful in the case where you do not have knowledge about either or are too busy or lazy to think about it.