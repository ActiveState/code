## LazyGettext  
Originally published: 2005-01-19 10:50:26  
Last updated: 2005-01-19 10:50:26  
Author: Shannon -jj Behrens  
  
In some code I have to work with but don't have much control over,
there are a bunch of strings declared at the module level.  I need to figure
out what all those strings are, and wrap them in something.  Once they are
wrapped, they must behave as strings, but lazily "translate" themselves
whenever used in order for internationalization to work.  Since each Web
request might request a different language, I can't just do this once and be
done with it.