## Find Prime Numbers in python 

Originally published: 2010-06-12 08:06:01
Last updated: 2010-06-12 08:22:40
Author: Giannis Fysakis

The algorithm is based on the idea  \nthat the next larger prime after one prime is the sum of the two smaller previous minus three prime numbers back. \nFor the first five prime numbers 2,3,5,7,11 this  pattern is not true also it is not true if the number is a composite number (including of course if the number's square root is integer). \n\nExample \ntrying to find the tenth prime\n\nso lets play with numbers 17(minus 3 from Next,position 7), 19(minus 2 from Next,position 8), 23(minus 1 from Next,position 9) and number Next at position 10 :\n\nhmmm ... if we add 19 and 23 we get 42, but 42 minus 17 equals 25 which isn't a prime :(\n\nIn order to correct this we assume that 25 is the next prime number ( temporary holding the tenth position)\nfinally to get the real Next prime number we take 23 + 25 = 48  , we subtract 19 and  we get 29 which finally it takes the tenth position ( because it deserves it :P)