## Probability Dictionary  
Originally published: 2010-11-12 20:13:33  
Last updated: 2010-11-14 08:52:51  
Author: Felipe   
  
A subclass of dictionary that ensures that values are nonnegative, less than or equal to 1, and sum to 1. It also gives 0 for any attempt at looking up a key not in it, and purges keys whose associated value falls to 0.