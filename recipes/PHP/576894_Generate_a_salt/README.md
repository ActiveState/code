## Generate a salt 
Originally published: 2009-09-01 19:04:43 
Last updated: 2012-07-10 19:52:17 
Author: Xavier L. 
 
This function will generate a salt for use with passwords ranging using characters in range a to z, A to Z, 0 to 9 and !@#$%&*?. The characters are sorted in a random value and can appear more than one time in the string. This way, this function is more powerful than the *shuffle()* function. This means that the salt could also be longer than the character list.\n\n 