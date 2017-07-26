###Evaluate upper-letters variable name as constants at compile time.

Originally published: 2005-06-29 02:27:10
Last updated: 2005-07-12 10:27:09
Author: Ikkei Shimomura

This code converts variables which is made with upper-leters only, into\nconstants at compile time, if it is possible to be replaced. and generate\n.pyc file.\n\nThis recipe pay attensions to the compile time evaluation,\nthe feature of Constants.