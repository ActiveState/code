## Creating a Local __dict__

Originally published: 2004-09-08 02:27:42
Last updated: 2004-09-08 14:40:27
Author: Derrick Wallace

Accessing the local namespace dict is already done by calling the builtin method locals(). However, the limitation of doing this is that modifying the dict returned by locals() is not considered 'safe'. Safe in the sense that any modifications are not guaranteed to be reflected in the actual namespace.\n\nIn order to implement a 'safe' reference and modification of the local dictionary, I use sys._getframe().f_locals.  This gives me direct access to the local dict each time I use it.  But beyond just having safe access to the local dict, I also would like a local __dict__ dict that acts exactly the way a class __dict__ would.  Currently, there is not a local __dict__ available.  So here is a way to create your own: