## Solving the Black-Scholes PDE with laplace inversion:RevisedOriginally published: 2010-03-25 06:51:32 
Last updated: 2010-04-06 13:26:02 
Author: Fernando Nieuwveldt 
 
I originally posted this code in Recipe 577132 and this is a repost of that recipe with corrections since there was an error in the original recipe. Added here is an error analysis to show the effectiveness of the Laplace inversion method for pricing European options. One can test the accuracy of this method to the finite difference schemes. The laplace transform of Black-Scholes PDE was taken and the result was inverted using the Talbot method for numerical inversion. For a derivation of the laplace transform of the Black-Scholes PDE, see for instance www.wilmott.com/pdfs/020310_skachkov.pdf.