## When to not just use socket.close()

Originally published: 2005-04-06 07:04:41
Last updated: 2005-04-08 17:31:14
Author: John Nielsen

I have implemented a "broken" client/server to show how socket.shutdown can be more useful than a simple socket.close operation. (I rewrote this to hopefully be more clear)\n\nThe close operation is not atomic. It implicitly tries to send any remaining data in _addition_ to closing a descriptor.  Splitting this close operation up with the aid of the shutdown command can help avoid bugs.  It gives the server one final way to say, "something went wrong". The server would also know that the client did not end correctly, since the socket should remain open when the client finished sending data. For example, if the function exits unexpectedly and python closes the socket for you, the server would not be able to send any data back.\n\nIn the server below, the client and server have different ideas about what the end marker should be. The rev_end function is written so as to look for an end marker. And, as long as they agree it should work. The socket.shutdown is for when something goes wrong.