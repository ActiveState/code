## Instantiating pickled instances transparently

Originally published: 2005-09-19 22:26:08
Last updated: 2005-09-19 22:26:08
Author: George Sakkis

This recipe addresses the following two needs:\n- Object construction for some class is expensive.\n- Objects of this class need to be instantiated across multiple runs of the program.\nFor example, object instantiaton may involve reading one or more big files, connecting to a database or a network socket with considerable expected delay, etc.\n\nThe autopickle decorator deals with this problem by wrapping the __init__ of the class. The first time a specific instance is created, it is also pickled to a file. In all subsequent attempts to create the same instance, the pickled instance is loaded and returned instead. If unpickling the file is faster than creating the instance normally, all but the first instantiations are faster than the normal one.\n\nThe instance determines the path of the file to be pickled to by calling its getPickleFilename() method. This takes the same arguments given in __init__ and it has the responsibility to specify a valid and distinct path for the instance.