## Automatic indentation of output based on frame stack

Originally published: 2005-04-26 13:27:42
Last updated: 2005-04-26 13:27:42
Author: Lonnie Princehouse

Output stream wrapper; possibly useful for debugging code with print statements.\n\nWhen write() is called, it makes a note of the calling frame.  The indentation level is equal to the number of frames in the call stack which have been previously noted.  See example.