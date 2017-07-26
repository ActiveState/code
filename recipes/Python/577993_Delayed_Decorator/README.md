## Delayed DecoratorOriginally published: 2011-12-20 04:28:54 
Last updated: 2011-12-20 06:37:15 
Author: Peter Donis 
 
This is a decorator wrapper class to delay decorating the base function until it is actually invoked. This can be useful when decorating ordinary functions if some decorator parameters depend on data that is only known at function invocation. It can also be used (and was written) to ensure that a decorated method of a class gets decorated once per instance instead of once per class; the use case that prompted this was the need to memoize a generator (see the [Memoized Generator](http://code.activestate.com/recipes/577992-memoize-generator/) recipe), but the implementation is general.