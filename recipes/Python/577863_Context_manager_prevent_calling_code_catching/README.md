###Context manager to prevent calling code from catching exceptions

Originally published: 2011-09-01 13:01:59
Last updated: 2012-06-17 09:20:56
Author: Oren Tirosh

The following context manager causes any exceptions raised inside it to print a stack trace and exit immediately. The calling scope is not given a chance to catch the exception.