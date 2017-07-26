## Easy State Pattern - support for implementing state machines  
Originally published: 2009-01-13 14:24:36  
Last updated: 2009-06-15 11:25:17  
Author: Rodney Drenth  
  
Provides is a module that gives support for implementing state machines. States are implemented as subclasses, derived from the state machine class.  Methods that are state dependant or which cause transitions are declared using decorators. Because states can be subclasses of other states, common behaviour among several states is easily supported.  The implementation allows for implementing multiple states or substates within a class.\n\nThis module best support statem achines implemeting controllers for embedded systems, implementing user interfaces, or in discrete event model simulation.\nParsers, which generally have many states and where you would need to define\na Transaction method for each different character encountered would be more easily implemented by other means.