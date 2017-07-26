## A class which keeps a (weak) reference to it's instances.

Originally published: 2005-12-10 22:14:37
Last updated: 2005-12-11 06:15:49
Author: S W

This recipe implements a base class, which allows derived classes to track instances in self.__instances__. It uses a WeakValueDictionary to store instance references.