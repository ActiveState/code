## Merge join for N iteratorsOriginally published: 2008-07-22 07:59:14 
Last updated: 2008-10-29 03:50:37 
Author: Joel Nothman 
 
Performs a merge join on any number of iterators with sorted, unique keys. I.e., iterate through the data in parallel, outputting successive keys and all corresponding values from each iterator, or None if not available.