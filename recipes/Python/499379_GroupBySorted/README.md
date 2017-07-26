###GroupBySorted

Originally published: 2007-01-16 10:32:14
Last updated: 2008-08-08 23:48:22
Author: Shannon -jj Behrens

Updated: Use itertools.groupby instead.  See my comment below.\n\nThis is a variation of itertools.groupby.  The itertools.groupby iterator assumes that the input is not sorted but will fit in memory.  This iterator has the same API, but assumes the opposite.