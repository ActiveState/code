## Loop over and descend into sequences in a recursion-proof way

Originally published: 2002-04-01 07:07:55
Last updated: 2002-04-01 15:12:18
Author: Wolfgang Lipp

This is a function to iterate over a container and its elements that checks for recursive traps. The condition for descending into elements is highly configurable (a list of type() results, or a callable). Spin-offs: a function to check for iterability in a loose and in a strict sense; a function to flatten a hierarchical container into a list of its elements.