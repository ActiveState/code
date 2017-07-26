###Timing out function

Originally published: 2004-10-11 00:43:49
Last updated: 2004-10-14 11:55:55
Author: chris wright

This recipe presents two ways to time out the execution of a callable. It relies on signal.SIGALRM; I've only tested in on MacOSX. One way (TimedOutFn) works on Python 2.3.4, and the second uses the decorator syntax introduced in 2.4a. In this version, I've used the code from John Speno's page (http://www.pycs.net/users/0000231/). He's done a better job of handling the signals, and I like the try/finally expression.