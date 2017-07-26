## Wrapping method calls (meta-class example)Originally published: 2003-05-04 08:23:52 
Last updated: 2003-05-04 15:49:40 
Author: Stephan Diehl 
 
A metaclass is used to wrap all (or just some) methods for logging purposes. The underlying mechanism can be used as well to check pre/post conditions, attribute access,...\nThe basic point is, that the actual class must not be changed in any way to achive the desired effect.