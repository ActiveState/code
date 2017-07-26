###try ... catch ... finally

Originally published: 2001-09-11 03:13:07
Last updated: 2001-09-11 03:13:07
Author: Donal Fellows

The Java try ... catch ... finally construct is really nice for those cases when you want to guarantee to always release a resource (particularly a file handle) even if the code generates an exception. It is also very useful to be able to use different types of error handling depending on the error that occurred. This code implements such a facility in pure Tcl.