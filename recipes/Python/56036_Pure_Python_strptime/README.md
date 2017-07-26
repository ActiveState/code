## Pure Python strptime  
Originally published: 2001-05-23 18:42:48  
Last updated: 2003-09-15 18:01:45  
Author: Brett Cannon  
  
This is a modification of the Python code that powers time.strptime() in CVS on 2003-08-11 (Python 2.4 development) to be compatible with Jython 2.1 and CPython 2.1 .  It does require the datetime package if you want missing date info to be filled in; it can be found in CVS at /python/nondist/sandbox/datetime/ .

If you are using CPython version 2.3.0 or higher, then you do not need this.  A more modernized version of the code is included in the language.