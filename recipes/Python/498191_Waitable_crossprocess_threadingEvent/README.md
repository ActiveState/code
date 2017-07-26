## Waitable, cross-process threading.Event class. 
Originally published: 2006-10-10 11:18:34 
Last updated: 2006-10-10 11:18:34 
Author: David Wilson 
 
This class implements an interface similar to threading.Event using os.pipe() as the mechanism for signalling. This allows the class to be used to wake up select.select() and select.poll() loops without having to peridiodically resume execution to check the status of an event.