## Iterator Algebra Implementations of Relational Join Algorithms 
Originally published: 2006-04-26 10:55:01 
Last updated: 2006-04-26 10:55:01 
Author: Jim Baker 
 
Implements the three standard relational join algorithms: nested loops join, hash join, and merge join, using the iterator algebra support in Python 2.4. This recipe presents code that can be used for inner join, left outer join, full outer join, and semijoins. The nested loops join supports a theta join.