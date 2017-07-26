## fast prime number list creator 
Originally published: 2004-07-17 09:12:38 
Last updated: 2004-07-17 09:12:38 
Author: Kazuo Moriwaka 
 
This function return a list of numbers which is less than argument.\nIt is much faster than other implementations which I test. At my machine, prime_numbers_less_than(100000) takes about 0.78sec.\nThis code is tested at Python 2.3.4 only.