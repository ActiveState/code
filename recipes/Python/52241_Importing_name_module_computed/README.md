## Importing a name from a module with a computed name  
Originally published: 2001-03-15 16:43:03  
Last updated: 2001-03-15 16:43:03  
Author: Jürgen Hermann  
  
This function allows you to do "from module import name", where both "module" and "name" are dynamic values (i.e. expressions or variables). For example, this can be used to implement a "plugin" mechanism to extend an application by external modules that adhere to some common interface.\n\nThis pattern is used in MoinMoin (http://moin.sourceforge.net/) to load extensions implementing variations of a common interface, like "action", "macro", and "formatter".