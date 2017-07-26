## Alternative to __del__ using weakrefs and metaclasses

Originally published: 2007-05-03 23:57:17
Last updated: 2007-05-03 23:57:17
Author: Adam Olsen

This is an ever-so-slightly over engineered solution to using weakrefs instead of __del__.  It provides a "core" object for all the attributes your cleanup code needs, then allows your main object to continue as normal by using descriptors.