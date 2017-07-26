## PHP Dollarfy Function  
Originally published: 2003-05-24 14:41:07  
Last updated: 2003-05-24 22:03:47  
Author: Alvin Estevez  
  
Dollarfy Function those the following things to a floating point number:

1. This function inserts a comma separator into every 3 digits.
For example: 100000.1252 will be 100,000.1252.

2. Round to the decimal number to the next significant figure.
For example: 100,000.1252 will be 100,000.13

3. Add a dollar sign to the number.
For example: 100,000.13 will be $100,000.13

Syntax:
dollarfy (Decimal Number, Decimal places);

Example:
dollarfy (100000.1252, 2);

Output will be:
$100,000.13 (Rounded to the second Decimal place)

Note: You will need the commify function for it to work. dollarfy() function needs the commify() function to work.