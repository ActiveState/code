## Observer pattern implemented with Descriptor class  
Originally published: 2012-02-14 23:43:52  
Last updated: 2012-02-14 23:43:53  
Author: Rodney Drenth  
  
The observer pattern is implemented using an observable descriptor.
One creates instances of observable in a class, which allows observers to
subscribe to changes in the observable. Assigning a value to the observable
causes the suscribers to be notified. An observable can subscribe to another  observable, in which case changes to the second propagate to subscribers of the first.
The subscribe method returns a Subscription object. When this object is deleted or becomes unreferenced, the subscription is cancelled.

This version compatible with Python 3.0
Example uses unittest to help in understanding the functionality.