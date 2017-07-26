###Regular Expression for generic sequences of symbols

Originally published: 2009-06-13 09:50:12
Last updated: 2009-06-13 09:51:38
Author: Emanuele Ruffaldi

Python regular expression are very powerful and efficient and they can be applied to the recognition of different types of sequences. This recipe shows how to match sequences of generic symbol set with the power of regular expression. The code uses a mapping from every entity into a character. The mapping is used both at level of sequence and in the compilation of the regular expression. When the symbol set is small it is possible to efficiently use 8 bit strings instead of full unicode.