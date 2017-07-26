## Calculate Pi using Monte Carlo Simulations in Python (Vectorized)  
Originally published: 2011-02-17 22:35:45  
Last updated: 2011-02-17 22:35:46  
Author: Zach Pace  
  
I saw something like this in C++ as an introduction to Monte Carlo, so I decided to make something similar in Python.  My original code used for loops, but I vectorized it with no small amount of effort, and it now runs orders of magnitude faster.  For example, I can calculate pi to .002% error with 100,000,000 randomized coordinates in approximately 15 seconds.  Careful to start small, because memory fills up quickly, and the computer will run slow if you overstep your RAM.  I'm able to go up to a bit more than 150 million without compromising speed and functionality in other tasks.

For those who are curious, vectorization is a technique whereby numpy (or similar) arrays replace things like loops.  They're a bit tricky to write (at least for me), but they work beautifully.

It might be useful for visualization to plot the occurrence of data points, and observe the randomness