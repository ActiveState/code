## Lazy Dynamic Binding on Classes (You'll Never Go Back)  
Originally published: 2011-06-11 00:02:36  
Last updated: 2011-08-12 23:42:27  
Author: Eric Snow  
  
This recipe provides a descriptor class and a decorator to make the deferred binding.  Before the first access to that name, the __dict__ of the class will have the descriptor object.  After that first access it will have whatever was returned by the first access.

One big advantage of deferring the binding is that the class object will be available at that time and can be passed to the object.  During normal class creation the class body is exec'd before the class object is created, so the objects bound there can't be passed the class.

Recipe #577746 provides a concrete example of how the deferred_binder can be used.