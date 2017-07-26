## A threading.Event you can pickle  
Originally published: 2006-02-07 07:59:16  
Last updated: 2006-02-07 07:59:16  
Author: Phil Groce  
  
Objects that use the Event object from the threading core library can't be pickled because the Event's underlying implementation is an unpicklable Lock object. Conceptually, though, an Event is just a boolean, so providing reasonable serialization behavior is pretty straightforward.