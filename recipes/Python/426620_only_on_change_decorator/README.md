## "only on change" decorator

Originally published: 2005-06-24 07:17:29
Last updated: 2005-06-24 07:17:29
Author: Alan McIntyre

This decorator runs a function/method the first time called, and on any subsequent calls when some user-defined metric changes.  The metric function provided to the decorator is called every time, but the function being decorated is only called on the first call and when the metric changes.