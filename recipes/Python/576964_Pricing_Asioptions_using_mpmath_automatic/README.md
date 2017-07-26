## Pricing Asian options using mpmath with automatic precision control  
Originally published: 2009-11-24 01:20:56  
Last updated: 2009-11-24 01:20:56  
Author: Dieter Kadelka  
  
In Recipe 576954 presented a numerical method for pricing Asian options using mpmath and some code from Recipe 576938: Numerical Inversion of the Laplace Transform with mpmath. The code in Recipe 576954 seems to have problems with the precision required for accurate computation of the integrals. To solve this problem, I changed the code in Recipe 576938 and the code in Recipe 576954, which now uses mp_laplace.py.\n\nThe new mp_laplace.py and asian.py are in the code section.