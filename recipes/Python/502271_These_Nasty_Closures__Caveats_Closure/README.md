## These Nasty Closures - Caveats for the Closure Enthusiast  
Originally published: 2007-03-03 11:31:05  
Last updated: 2007-03-03 11:31:05  
Author: Zoran Isailovski  
  
Closures are powerful. Closures are beautiful. But: Closures are TRICKY!

This is an anti-recipe, a caveat about some obscure pitfalls with closures - or the way they are implemented in python.

And now for the caveats: Two no-no's...

1. Don't create more then one instance of the same closure per normal function!

2. Don't create more then one instance of the same closure per generation cycle in a generator function!

Here is why...