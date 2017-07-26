## How to define multiple initializers for a class, with different arguments  
Originally published: 2003-09-18 22:48:41  
Last updated: 2008-07-30 08:36:56  
Author: Paul McGuire  
  
Sometimes your class design warrants the definition of multiple construction methods for a class, such as rebuilding from a serialized form vs. normal internal construction with explicit parameters.  This recipe gives an example of using class level methods to create such constructors.