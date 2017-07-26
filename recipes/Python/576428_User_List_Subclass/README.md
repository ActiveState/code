## User List Subclass

Originally published: 2008-08-18 16:24:36
Last updated: 2008-08-18 09:26:07
Author: nosklo 

As subclassing list has a problem when using __getitem__, __delitem__ and __setitem__ methods with slices (they don't get called because parent implements __getslice__, __delslice__ and __setslice__ respectively), I've coded this UserList class that is a subclass of list, but overwrites these methods.\nBy subclassing this class, you can overwrite __getitem__ and it will be called correctly for slices.