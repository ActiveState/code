## Using re.match, re.search, and re.group in if ... elif ... elif ... else ...Originally published: 2005-11-15 19:36:32 
Last updated: 2005-11-16 12:03:18 
Author: Peter Kleiweg 
 
A wrapper class for (a small part of) the 're' module, that enables you to do re.match() or re.search() in an 'if' test or 'elif' test and use the result of the match after the test.