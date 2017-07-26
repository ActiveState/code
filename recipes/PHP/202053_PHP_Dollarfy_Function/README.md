## PHP Dollarfy Function

Originally published: 2003-05-24 14:41:07
Last updated: 2003-05-24 22:03:47
Author: Alvin Estevez

Dollarfy Function those the following things to a floating point number:\n\n1. This function inserts a comma separator into every 3 digits.\nFor example: 100000.1252 will be 100,000.1252.\n\n2. Round to the decimal number to the next significant figure.\nFor example: 100,000.1252 will be 100,000.13\n\n3. Add a dollar sign to the number.\nFor example: 100,000.13 will be $100,000.13\n\nSyntax:\ndollarfy (Decimal Number, Decimal places);\n\nExample:\ndollarfy (100000.1252, 2);\n\nOutput will be:\n$100,000.13 (Rounded to the second Decimal place)\n\nNote: You will need the commify function for it to work. dollarfy() function needs the commify() function to work.