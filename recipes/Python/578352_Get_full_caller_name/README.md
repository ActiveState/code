## Get full caller name (package.module.function)Originally published: 2012-11-30 21:54:46 
Last updated: 2012-11-30 21:54:46 
Author: anatoly techtonik 
 
This function allows to get fully qualified name of the calling function. I expected this field to be available from logging module, but it is not here http://docs.python.org/2/library/logging.html#logrecord-attributes It might be that it is too expensive for performance or just doesn't play well in some situations. I don't know. I use it solely when debugging and it is convenient.\n\nAlso here: https://gist.github.com/2151727