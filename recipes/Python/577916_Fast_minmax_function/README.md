## Fast min/max function 
Originally published: 2011-10-22 18:40:32 
Last updated: 2011-10-22 18:40:32 
Author: Raymond Hettinger 
 
Minimizes the number of comparisons to compute the minimum and maximum of a dataset.  Uses 1.5 compares for every element, improving on the more obvious solution that does 2 comparisons per element.