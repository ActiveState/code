## Generating correlated random numbers  
Originally published: 2008-09-21 21:21:52  
Last updated: 2008-09-21 21:21:52  
Author: Kaushik Ghose  
  
From this great [tutorial][sitmo]

  [sitmo]: http://www.sitmo.com/doc/Generating_Correlated_Random_Numbers

For two corelated variables, the formula is much as one would get from intuition about the meaning of correlation with some twist due to normalizing the standard deviation:
$X_3 = \alpha X_1 + \sqrt{1-\alpha^2} X_2$
Where $X_1$ and $X_2$ are two independent random variables, and $\alpha$ is the coefficient of correlation between $X_1$ and $X_3$.

In a more general sense:  
Let $C$ be the correlation matrix desired. Let $X_1, X_2..., X_N$ be $N$ independent random variables arranged in a row matrix $R = [X_1, X_2,....,X_N]$. Then 
$Q = RU$
where
$U^TU = C$
gives us $N$ random variables $Q = [Y_1, Y_2, ..., Y_N]$ with the required property.