## REAL case insensitive string replace

Originally published: 2009-04-09 15:03:42
Last updated: 2009-04-25 15:48:50
Author: Jonas Haag

REAL case insensitive version of `str.replace` that keeps the letter case of the original expression (Doesn't only replace `Foo` and `foo` to `...foo...` but to `...Foo..` and `...foo...`).