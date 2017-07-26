## "public" decorator, adds an item to __all__  
Originally published: 2009-12-30 12:53:29  
Last updated: 2009-12-30 12:53:29  
Author: Sam Denton  
  
The DRY principle says, "Don't repeat yourself".  A Python module typically defines a global variable named "__all__" that holds the names of everything the author wants visible.  This means you have to type each function or class name a second time, and you have to maintain the contents of __all__ manually.  This fixes that.