## Normalizing newlines between windows/unix/macs 
Originally published: 2005-07-02 14:28:58 
Last updated: 2005-07-02 14:28:58 
Author: Ori Peleg 
 
When comparing text generated on different platforms, the newlines are different. This recipe normalizes any string to use unix-style newlines.\n\nThis code is used in the TestOOB unit testing framework (http://testoob.sourceforge.net).