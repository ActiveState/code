## Generating correlated random numbers  
Originally published: 2008-09-21 21:21:52  
Last updated: 2008-09-21 21:21:52  
Author: Kaushik Ghose  
  
From this great [tutorial][sitmo]\n\n  [sitmo]: http://www.sitmo.com/doc/Generating_Correlated_Random_Numbers\n\nFor two corelated variables, the formula is much as one would get from intuition about the meaning of correlation with some twist due to normalizing the standard deviation:\n$X_3 = \\alpha X_1 + \\sqrt{1-\\alpha^2} X_2$\nWhere $X_1$ and $X_2$ are two independent random variables, and $\\alpha$ is the coefficient of correlation between $X_1$ and $X_3$.\n\nIn a more general sense:  \nLet $C$ be the correlation matrix desired. Let $X_1, X_2..., X_N$ be $N$ independent random variables arranged in a row matrix $R = [X_1, X_2,....,X_N]$. Then \n$Q = RU$\nwhere\n$U^TU = C$\ngives us $N$ random variables $Q = [Y_1, Y_2, ..., Y_N]$ with the required property.