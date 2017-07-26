## Testing for an empty iteratorOriginally published: 2005-05-09 06:17:51 
Last updated: 2005-05-17 15:51:08 
Author: Michael Chermside 
 
With lists, it is common to test whether the list is empty and perform special code for the empty case. With iterators, this becomes awkward -- testing whether the iterator is empty will use up the first item! The solution is an idiom based on itertools.tee().