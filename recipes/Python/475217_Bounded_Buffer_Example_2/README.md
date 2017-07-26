## Bounded Buffer Example (2) 
Originally published: 2006-03-29 10:11:15 
Last updated: 2006-03-29 10:11:15 
Author: Stephen Chappell 
 
This is the second example solution to the bounded\nbuffer problem. By looking at the code, you may\nnotice that it has several features that exapand\non what is demonstrated in the first example.\nFirst of all, it accepts several new command line\narguments that allow customization of the operation\nof this recipe (including an optional seed argument).\nFurthermore, this recipe features a fourth thread\nthat takes care of printing for the producer and\nconsumer threads. Of all the improvements in this\nexample, one of the nicest involves improved\nfunctions for the threads being executed.