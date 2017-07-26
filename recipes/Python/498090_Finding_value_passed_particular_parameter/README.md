## Finding the value passed for a particular parameter to a function by name

Originally published: 2006-09-12 11:01:44
Last updated: 2006-09-14 15:57:06
Author: Jacob Smullyan

Sometimes inside a decorator that creates a function with a generic (*args, **kwargs) signature, you want to access a value passed for a particular parameter name to a wrapped function, but don't know whether that value will be passed as a positional or keyword argument, or whether the wrapped function defines a default value for the parameter.  The following utility function extracts this information for you.