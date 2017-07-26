## Gaussian integration with or without Log singularityOriginally published: 2009-09-09 21:03:10 
Last updated: 2009-09-09 21:03:10 
Author: Gabriel Genellina 
 
The Gaussian quadrature is among the most accurate integration scheme for smooth integrands. It replaces a integral by a sum of sampled values of the integrand function times some weight factors.\n\nThis is strictly a minor rewrite of recipe 52292, just to make it compatible with Python 2.4 and above. 2to3 converts it perfectly to be used with Python 3.x\n\n*All* credit is due to the original author, Alexander Pletzer.