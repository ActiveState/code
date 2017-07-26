## strsignal  
Originally published: 2014-06-29 15:47:23  
Last updated: 2014-06-29 15:47:24  
Author: Zack Weinberg  
  
This is an emulation of the standard (POSIX.1-2008) C library function [`strsignal()`](http://pubs.opengroup.org/onlinepubs/9699919799/functions/strsignal.html), which should be in the [`signal` module](https://docs.python.org/3/library/signal.html), but isn't.

If possible, it uses [`ctypes`](https://docs.python.org/3/library/ctypes.html) to call the C library function; otherwise, it tries to build a reverse mapping of the `SIG*` constants in the signal module; if that doesn't work either, it just produces `"signal %d"` where `%d` is the decimal signal number.

If invoked as a script, will test all of the strategies and print the results.

Tested in 2.7 and 3.4; *should* work with 2.6 and 3.3 as well.