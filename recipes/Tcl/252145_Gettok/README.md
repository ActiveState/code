## Gettok  
Originally published: 2003-11-18 00:55:23  
Last updated: 2003-11-20 07:58:29  
Author: Kiko The King  
  
It returns the Xth token in a sentence..
like: i have a sentence divided by : and i want to get the second value
sentence:
set x "Value 1 : Value 2 : Value 3"
[gettok $x 2 :]
is returns <b>Value 2</b>
if you use 0 as the number...it will returns the number of tokens
in this case... <b>3</b>