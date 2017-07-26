## Observer pattern implemented with Descriptor class

Originally published: 2009-12-08 14:05:19
Last updated: 2010-03-13 11:53:18
Author: Rodney Drenth

The observer pattern is implemented using an observable descriptor.\nOne creates instances of observable in a class, which allows observers to\nsubscribe to changes in the observable. Assigning a value to the observable\ncauses the suscribers to be notified. An observable can subscribe to another  observable, in which case changes to the second propagate to subscribers of the first.\nThe subscribe method returns a Subscription object. When this object is deleted or becomes unreferenced, the subscription is cancelled.