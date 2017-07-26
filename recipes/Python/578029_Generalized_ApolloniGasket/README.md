## Generalized Apollonian Gasket Fractal  
Originally published: 2012-02-01 02:49:09  
Last updated: 2012-02-01 02:49:09  
Author: FB36   
  
It draws Apollonian Gasket Fractal for any n using Descartes theorem.

This is not the standard way though. It simply randomly finds 3 tangent circles at each iteration and tries to add new circles. The good thing is it can start w/ any arbitrary configuration of main circles, unlike the standard way. The bad thing is some circles will stay missing because of random selections they never get a chance. You can increase the maxIt to get better result but it would slow it down a lot.