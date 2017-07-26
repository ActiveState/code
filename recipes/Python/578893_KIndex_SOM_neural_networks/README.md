## KIndex for SOM neural networks (Python)  
Originally published: 2014-06-16 13:20:00  
Last updated: 2014-06-16 13:20:01  
Author: Roberto Bello  
  
Achieved cataloging into groups by a SOM neural network, the question arises
whether or not there is knowledge in the groups, namely whether the groups are between them
distinct and have homogeneous characteristics within each group.
The use of the coefficient of variation (CV) can be of help.

KINDEX (Knowledge Index) is an index that measures how much knowledge is
contained in the groups obtained from the SOM neural network: in the case KINDEX
reaches the maximum value of 1, each group would consist of records with constant 
values ​​in all the variables / columns, and each group would be quite distinct 
from other groups.
KINDEX is calculated using the weighted-average CV of variables / columns
groups, comparing them to the CV of the variables / columns of the input file before
cataloging.