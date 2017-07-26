## Total Ordering: Class Decorator for Filling in Rich Comparison Methods When Only One is Implemented  
Originally published: 2008-10-05 19:57:34  
Last updated: 2008-10-28 11:54:42  
Author: Michael Foord  
  
``total_ordering`` and ``force_total_ordering`` are class decorators for 
Python 2.6 & Python 3.

They provides *all* the rich comparison methods on a class by defining *any*
one of '__lt__', '__gt__', '__le__', '__ge__'.

``total_ordering`` fills in all unimplemented rich comparison methods, assuming
at least one is implemented. ``__lt__`` is taken as the base comparison method
on which the others are built, but if that is not available it will be
constructed from the first one found.

``force_total_ordering`` does the same, but having taken a comparison method as
the base it fills in *all* the others - this overwrites additional comparison
methods that may be implemented, guaranteeing consistent comparison semantics.
