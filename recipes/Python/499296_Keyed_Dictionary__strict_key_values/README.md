## Keyed Dictionary -- strict key values in a dictionary 
Originally published: 2006-12-04 13:53:18 
Last updated: 2006-12-04 21:52:58 
Author: Mike Hostetler 
 
The KeyedDict object keeps a list of approved key values.  If you try to assigned an unapproved key to a value, an exception is thrown.\n\nWhen you create the object, you give it a sequence (tuple, list, etc.) of key objects and then, when you set an item with a key, it will make sure that the key is in the "approved" list.  If you try to set an item with a key that isn't in your approved list, you get an TypeError exception.