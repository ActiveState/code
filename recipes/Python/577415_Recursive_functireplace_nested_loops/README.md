###Recursive function to replace nested for loops (cartesian product)

Originally published: 2010-10-01 00:35:47
Last updated: 2010-10-01 00:40:26
Author: Kieran 

Same functionality as the itertools product method (http://docs.python.org/library/itertools.html#itertools.product) with one major difference: generators are executed as the loop executes. An itertools product causes all the variables to be collected before the loop actually starts looping.