## Dynamic function composition decoratorOriginally published: 2007-09-06 02:36:53 
Last updated: 2007-09-06 02:36:53 
Author: kay schluehr 
 
This pattern describes a way to add or remove behaviour to/from a function dynamically. This is not possible by just stacking decorators. Instead the callables used for the function composition will be hold independently by a Composer object.