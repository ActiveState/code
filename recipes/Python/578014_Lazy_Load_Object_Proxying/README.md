## Lazy Load Object Proxying

Originally published: 2012-01-13 07:56:28
Last updated: 2012-01-13 07:56:29
Author: Cory Virok

A very slight modification on Tomer Filiba's original Proxy class to use a factory function instead of an instance to create an object proxy the first time it is required. The only other modification is to add an instance variable to LazyLoadProxy to store data specific to the proxy and not the delegated instance. 