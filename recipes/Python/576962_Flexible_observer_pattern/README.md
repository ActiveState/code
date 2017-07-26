## Flexible observer pattern implementationOriginally published: 2009-11-20 13:04:03 
Last updated: 2012-12-06 19:23:11 
Author: Glenn Eychaner 
 
A simple, flexible, general-purpose observer pattern.\n\nObservers can be callable objects or objects with a particular named method (handle_notify() by default).  Events can be any object, and observers can select which events they are interested in receiving.  Support for a number of different types of lightweight event objects is included.\n