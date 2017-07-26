###General dispatching mechanism for C#-style events

Originally published: 2005-07-03 17:34:34
Last updated: 2005-07-03 17:34:34
Author: Steven Cummings

This is an dynamic dispatching approach inspired by C#-style events. The approach allows for the dispatch of an event to a series of chained methods through the use of a Dispatcher. The Dispatcher can be defined either as part of a class or merely as a variable in some code. When the Dispatcher is invoked the methods that are chained to it (i.e. handlers) are invoked. The dispatch can be either blocking or non-blocking, and is non-blocking by default.