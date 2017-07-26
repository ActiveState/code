## A Protocol for Making Objects Immutable

Originally published: 2011-10-07 01:52:39
Last updated: 2011-10-07 03:59:45
Author: Eric Snow

Python already provides immutable versions of many of the mutable built-in types.  Dict is the notable exception.  Regardless, here is a protocol that objects may implement that facilitates turning immutable object mutable and vice-versa.