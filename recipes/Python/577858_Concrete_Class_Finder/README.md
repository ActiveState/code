## Concrete Class FinderOriginally published: 2011-08-24 05:29:14 
Last updated: 2011-08-24 05:29:15 
Author: Lucio Santi 
 
This recipe implements a design pattern useful for performing an object-oriented case analysis for a particular object (or a collection of objects as well). Essentially, it is an alternative to complex if-then-else or switches. Modelling each case with a particular class, the Concrete Class Finder searches for an appropriate case/class that applies to the given object/s. Once found, this class can be used in an homogeneous way, independently of the object/s previously considered.