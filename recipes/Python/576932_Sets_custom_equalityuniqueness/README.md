## Sets with a custom equality/uniqueness function

Originally published: 2009-10-18 13:13:45
Last updated: 2009-10-29 21:08:22
Author: Gabriel Genellina

The builtin `set` and `frozenset` types are based on object equality; they call __eq__ to determine whether an object is a member of the set or not.  But there are cases when one needs a set of objects that are compared by other means, apart from the default __eq__ function.  There are several ways to achieve that; this recipe presents two classes, FrozenKeyedSet and KeyedSet, that take an additional function `key` which is used to determine membership and uniqueness.  Given two objects which return the same value for `key`, only one of them will be in the set.