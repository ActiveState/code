## Implementing a circular data structure using lists 
Originally published: 2001-03-13 18:16:59 
Last updated: 2001-03-13 18:16:59 
Author: Chris McDonough 
 
In some applications, it's advantageous to be able to define a circular data structure (a structure in which the last element is a pointer to the first).  Python lists make it easy to make such a beast.  A list is an ordered sequence of elements, so implementing a "ring" as a Python list is easy.  "Turning" the ring consists of removing the last element from the list and placing it in the list's beginning slot.  We can encapsulate this behavior in a class, which is shown below as the "Ring" class.