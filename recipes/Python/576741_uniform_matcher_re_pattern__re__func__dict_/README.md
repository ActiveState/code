## uniform matcher( "re pattern" / re / func / dict / list / tuple / set )  
Originally published: 2009-05-06 04:27:20  
Last updated: 2009-05-06 06:17:16  
Author: denis   
  
matcher() makes a string matcher function from any of:

* "RE pattern string"
* re.compile()
* a function, i.e. callable
* a dict / list / tuple / set / container

This uniformity is simple, useful, a Good Thing.

A few example functions using matchers are here too: grep getfields kwgrep.