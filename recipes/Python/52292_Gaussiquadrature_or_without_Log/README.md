###Gaussian quadrature with or without Log singularity

Originally published: 2001-03-21 10:02:08
Last updated: 2001-04-05 20:31:05
Author: Alexander Pletzer

If you have the freedom to choose your abscissas and your integrand is smooth or has\na log singularity, then this script is for you. It computes the definite integral of a user\ndefined function over the interval [a, b]. The user can specify the number of Gauss\npoints (1 <= ng <= 12), the default being ng=10.