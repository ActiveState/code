## These Nasty Closures - Caveats for the Closure Enthusiast  
Originally published: 2007-03-03 11:31:05  
Last updated: 2007-03-03 11:31:05  
Author: Zoran Isailovski  
  
Closures are powerful. Closures are beautiful. But: Closures are TRICKY!\n\nThis is an anti-recipe, a caveat about some obscure pitfalls with closures - or the way they are implemented in python.\n\nAnd now for the caveats: Two no-no's...\n\n1. Don't create more then one instance of the same closure per normal function!\n\n2. Don't create more then one instance of the same closure per generation cycle in a generator function!\n\nHere is why...