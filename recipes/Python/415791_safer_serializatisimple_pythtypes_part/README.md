## safer serialization of simple python types, part two  
Originally published: 2005-06-02 01:34:03  
Last updated: 2005-06-13 07:00:35  
Author: S W  
  
This recipe is a reimplemtation of this recipe,

http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/415503

using Python 2.4 decorator syntax.

It also has added support for boolean and unicode types, and a keyword argument (compress=False) for the dumps function, which will compress the string.