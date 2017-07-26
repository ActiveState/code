## Infix operators for numpy arrays 
Originally published: 2010-04-19 05:20:50 
Last updated: 2010-06-07 05:57:07 
Author: John Schulman 
 
This recipe adapts the infix operator trick from http://code.activestate.com/recipes/384122-infix-operators/ to give the appropriate behavior with numpy arrays, so you can write A \\*dot\\* B for np.dot(A,B)\n\nUPDATE\nA solution to the dot problem was recently added to the numpy trunk: the dot method was added to the ndarray class so you can write a.dot(b). See http://projects.scipy.org/numpy/ticket/1456