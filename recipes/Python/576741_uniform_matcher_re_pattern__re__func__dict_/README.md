## uniform matcher( "re pattern" / re / func / dict / list / tuple / set )

Originally published: 2009-05-06 04:27:20
Last updated: 2009-05-06 06:17:16
Author: denis 

matcher() makes a string matcher function from any of:\n\n* "RE pattern string"\n* re.compile()\n* a function, i.e. callable\n* a dict / list / tuple / set / container\n\nThis uniformity is simple, useful, a Good Thing.\n\nA few example functions using matchers are here too: grep getfields kwgrep.