## Enforce __all__ outside the 'import *' antipattern.  
Originally published: 2011-05-12 03:27:54  
Last updated: 2011-05-12 03:30:41  
Author: Daniel Holth  
  
__all__ is supposed to define a module's API. This class lets you know when that contract is violated by raising a warning. As an alternative, raise AttributeError() instead to __all__ with an iron fist.