## Barebones VC++ code: invoking Python COM factory and factory-made COM object  
Originally published: 2002-07-27 11:44:45  
Last updated: 2002-07-27 11:44:45  
Author: Bill Bell  
  
Two items:

1. Python script that defines and registers a factory COM class and another COM class that can be instantiated by the factory.
2. (Ugly) VC++ code that exercises the factory and then the object returned by the factory.

The Python COM object returned by the factory provides rudimentary stemming; ie, it removes any final 's' from a word that is passed to it and returns the truncated word as its result.