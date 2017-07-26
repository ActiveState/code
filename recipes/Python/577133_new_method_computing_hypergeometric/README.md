## A new method for computing the hypergeometric function 1F1(a,b,t) 
Originally published: 2010-03-21 10:05:53 
Last updated: 2010-03-22 05:00:20 
Author: Fernando Nieuwveldt 
 
I present a method of computing the 1F1(a,b,x) function using a contour integral. The method is based on a numerical inversion, basically the Laplace inversion. Integral is 1F1(a,b,x) = Gamma(b)/2\\pi i \\int_\\rho exp(zx)z^(-b)(1+x/z)^(-a)dz, \\rho is taken as a Talbot contour. The Talbot method is applied with the use of the midpoint rule for numerical integration. Here the user must give the number of function evaluations and this may vary from problem to problem. It is very easy to implement with only a few lines of code and it is very accurate even for large arguments.