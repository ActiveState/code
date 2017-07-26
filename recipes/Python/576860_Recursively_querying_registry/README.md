## Recursively querying for registry subkeysOriginally published: 2009-07-28 03:13:53 
Last updated: 2009-07-28 03:23:29 
Author: Heinz Hermann 
 
Because the Windows XP API does not support the RegDeleteTree function, the programmer has to query for subkeys of a registry key recursively, before he can delete it. This functions returns all subkeys of a registry key in deleteable order, which means the deepest subkey is the first in the list. 