## Adding __implements__ to subclasses during ABCMeta.register

Originally published: 2011-05-20 23:48:19
Last updated: 2011-08-13 03:49:26
Author: Eric Snow

This is an extension to the abc.ABCMeta class.  It is related to recipe 577711.\n\nBasically it has ABCMeta.register add __implements__ to any subclass that gets registered.