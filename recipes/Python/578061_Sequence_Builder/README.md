## Sequence Builder  
Originally published: 2012-03-03 14:36:56  
Last updated: 2012-03-03 17:50:03  
Author: Thomas Lehmann  
  
**Why?**
 * Thinking about a sequence of odd numbers where numbers divisible by 3 are not part of it I came to  a sequence starting with 5, 7, 11, 13, 17, 19, ...
 * The interesting property of this sequence is that the sequence of differences between the individual elements are 2,4,2,4,2,...

**How?**
 * I'm not a math expert (unfortunately) but I could imagine that there is a quite simple formula to get this.
 * However I thought that using different combinations of defined functions a script could do the favour for me.

**Result?**
 * Formula: `(((-1)**(x-1))+1)+2` -> Simplified -> `-1**(x-1) + 3` (now clear to you?)
 * You have to look for the sequence [4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2]

**Out of scope:**
 * Does not check for using lambda functions only and "x" only in the lambda functions.
 * The Python script does not simplify functions like changing ((x+1)+1) to x+2 - would be an interesting recipe - by the way :)

**Please note**
 * You should not add other functions than lambda.
 * You should always use "x" in your formular.
 * Be aware that the actual setup runs a few minutes (about 3 minutes) and you can imagine - surely - that adding further functions will definitely increase the runtime.

**Side effects?**
 * Quite funny to produce a sequence of nines with `(((-1)**(2*x))+2)**2`.
 * If you apply the first binomial theorem (a+b)^2 = a^2 + 2ab + b^2 then you see why!

**What I have learned from this?**
 * The biggest nightmare I did have with the Sequence class because of not knowing how to generate unique elements of this in a set (__eq__ and __hash__ are required); and I have to ensure that the hash code is calculated once only.
 * The 'combineFunctions' was interesting to me. I have never used 'inspect.getsource' before.
 * A few minutes does not sound much but for developing all times with more than 30 seconds are not comfortable. There are just 325 sequences and to investigate for certain sequences you probably have to have some more formula. Maybe I would have to take another approach for that.
