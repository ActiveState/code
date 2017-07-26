## Convert from decimal to any base number 
Originally published: 2001-06-14 21:26:23 
Last updated: 2004-06-30 20:33:14 
Author: Brett Cannon 
 
This function takes in any base-10 integer and returns the string representation of that number in its specified base-n form.\n\nUp to base-36 is supported without special notation for symbolizing when a number is really in a single digit position.  When that does occur, the number that takes up that single base is surrounded by parantheses.\n\n[2004-06-30: Renamed function to base10toN to be more proper]\n\n[2001-06-17: Changed comments to base-36 instead of base-35; thanks Klaus Alexander Seistrup]\n\n[2001-06-17: Added for loop mechanism in Discussion for alternative way of creating num_rep dictionary; thanks Hamish Lawson for suggesting that possibility]