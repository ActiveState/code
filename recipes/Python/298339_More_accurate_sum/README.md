## More accurate sum  
Originally published: 2004-08-04 00:27:54  
Last updated: 2004-08-05 10:25:59  
Author: Yaroslav Bulatov  
  
Built-in "sum" function, as well as add.reduce functions in Numeric/numarray introduce a large error when summing large arrays of like elements. I got relative error of about 1e-9 after summing 10 million doubles between 0 and 1. Function below has error less than 1e-15, doesn't use any additional memory (although it destroys the data array), and also runs asymptotically faster for unlimited precision numbers.