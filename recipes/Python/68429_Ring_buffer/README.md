## Ring buffer

Originally published: 2001-09-21 07:13:51
Last updated: 2001-09-24 12:42:54
Author: Sébastien Keim

A ring buffer is a buffer with a fixed size. When it fills up, adding another element overwrites the first. It's particularly useful for the storage of log information. There is no direct support in Python for this kind of structure but it's easy to construct one.\n\nHere is a suggestion of implementation optimized for element insertion.