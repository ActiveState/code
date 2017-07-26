## Multiprocess-safe logging file-handler + interprocess RLock  
Originally published: 2010-09-19 01:34:53  
Last updated: 2010-09-22 17:30:10  
Author: Jan Kaliszewski  
  
A Python 2.x/3.x-compatibile **multiprocess-safe logging file-handler** (logging.FileHandler replacement, designed for logging to a single file from multiple independent processes) together with a simple **interprocess recursive lock** -- universal abstract classes + Unix/Linux implementation.

**Update:** It's is a deeply revised version. Especially, now it --

* is Python 2.4, 2.5, 2.6, 3.1 -compatibile (previously Py>=2.6 was needed); probably works also with 2.7, 3.0 and 3.2 (but not tested if it does);
* is multiprocess-safe as well as thread-safe (proviously thread safety within a process was missed);
* is based on public interfaces only (previously FileHandler._open() was called and overriden);
* implement full RLock instance interface, as documented for threading.RLock (previously non-blocking mode and context-manager interface were missing).

The module contains:

* Unix/Linux-only example implementation (with flock-based locking):
  **FLockRLock** and **FLockFileHandler** classes.
* universal abstract classes -- which may be useful at developing implementation for non-Unix platforms:
  **MultiprocessRLock**, **MultiprocessFileHandler**, **LockedFileHandler**,

Also a quick-and-dirty test was added.

**It is still an alpha version -- I'll be very grateful for any feedback.**

----

**Further updates:**

* 2010-09-20: Some corrections, especially: non-blocking mode bug in MultiprocessRLock.acquire() fixed; _test() function improved; plus fixes in the description below.

* 2010-09-22: _test() improved and moved to description section. Mistaken copyright-notice removed.