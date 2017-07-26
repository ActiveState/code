###Number to string in arbitrary base

Originally published: 2005-02-02 04:56:21
Last updated: 2005-02-02 04:56:21
Author: Nick Coghlan

The function <code>num_in_base</code> can be used to print a number using an arbitrary base. It allows numbers to be padded to a minimum field width, and can display negative numbers in a complemented format instead of with a leading negative sign.\n\nThe digits used can be overriden with an arbitrary sequence.