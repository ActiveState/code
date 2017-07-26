## Implementing Vertical Editing in Komodo 6

Originally published: 2010-09-23 21:41:49
Last updated: 2010-09-29 19:09:35
Author: Eric Promislow

When editing a group of similar lines, it's very convenient to be able to press down-arrow\nand move to the same starting column position on the next line.  (See an example at\nhttp://community.activestate.com/forum/vertical-editing ).\n\nThis code is for a Komodo 6 macro -- possibly the only tweak necessary to make it work on Komodo 5 is by commenting out the "macro.save()" code, but I haven't tested it.  The discussion below will talk about how to use it.  