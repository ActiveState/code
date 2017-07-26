###Multicontext (e.g. asynchronous) inline execution framework using coroutines

Originally published: 2009-11-24 11:19:24
Last updated: 2012-12-06 19:32:20
Author: Glenn Eychaner

A framework for executing inline code, contained in a generator, across multiple execution contexts, by pairing it with an executor that handles the context switching at each yield. An example of a generator which executes some iterations synchronously and some asynchronously is provided.  The framework is general enough to be applied to many different coroutine situations.\n