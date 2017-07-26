## SuperFly:  Separating class heirarchy from class definition.Originally published: 2009-02-15 20:43:57 
Last updated: 2009-02-15 20:47:51 
Author: Ted Skolnick 
 
This is a recipe for defining class hierarchies outside of class definitions.  This way you could at, runtime, decide what class should act as the parent of a given class.   A class could sometimes have one parent, sometimes another.