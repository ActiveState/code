## NamedShare -- Quasi-Singleton Metaclass  
Originally published: 2004-07-07 08:49:10  
Last updated: 2004-08-25 16:10:25  
Author: Samuel Reynolds  
  
NamedShare is a variation on the Singleton pattern (see http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/102187). In effect, it provides for a set of quasi-singletons, identified by keyword. If no keyword is given, the default share is accessed.