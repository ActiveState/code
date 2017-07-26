## Generator with lookahead  
Originally published: 2013-09-24 10:37:01  
Last updated: 2013-09-24 10:44:56  
Author: Rutger Saalmink  
  
Python generators are a great way of reducing memory usage due to the lazy (on demand) generation of values. However, when the process-time of generating such a value is relatively high, we can improve performance even more by obtaining the next n values of the generator in a separate thread in the background. Hence, the BackgroundGenerator.