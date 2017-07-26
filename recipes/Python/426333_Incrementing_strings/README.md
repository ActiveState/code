## Incrementing strings

Originally published: 2005-06-22 02:04:48
Last updated: 2005-06-22 02:04:48
Author: Simon Brunning

The story behind this one is that I was building a database conversion utility, converting both schema and data from one database engine to another. Thing was, the target database only allows 10 characters in its table and column names. I stripped down the longer entity names by removing whitespace and spacing characters, then non-leading vowels, and at the last resort, I truncated.\n\nThis worked on the whole, but I was getting the occasional duplicate, so I came up with this.