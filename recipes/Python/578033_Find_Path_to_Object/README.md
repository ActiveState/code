###Find Path to Object

Originally published: 2012-02-05 07:07:33
Last updated: 2012-02-05 07:07:33
Author: Stephen Chappell

After wondering what the easiest what to access one object from another was, the following functions were written to automatically discover the shortest path possible. The `find` function takes the item to find and the object to find it from and tries finding out the best access path. The optional arguments control the search depth, memory usage, et cetera. The `nth` function is a helper function for accessing data containers that cannot be indexed into. As a final note, line thirteen (`while candidates:`) will probably never evaluate to false.