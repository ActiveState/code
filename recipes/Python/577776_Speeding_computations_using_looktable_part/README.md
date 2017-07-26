## Speeding up computations using a lookup table part I 
Originally published: 2011-07-02 15:14:33 
Last updated: 2011-07-02 15:14:33 
Author: Kaushik Ghose 
 
I needed to use the cumulative normal distribution and normal probability density functions repeatedly for some data analysis. I found that I could speed things up drastically by using a lookup table and matplotlib's builtin interpolation function.