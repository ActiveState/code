## Quote python strings for safe use in POSIX shells  
Originally published: 2006-10-16 10:30:58  
Last updated: 2006-10-16 10:30:58  
Author: Richard Philips  
  
Often one has to quote a python string so that the result can be used as an argument to a command running in a POSIX shell.

The function QuoteForPOSIX can be used with sh, bash, csh, ksh