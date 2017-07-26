## Progress bar class

Originally published: 2002-12-11 12:53:21
Last updated: 2002-12-11 12:53:21
Author: Randy Pargman

Here is a little class that lets you present percent complete information in the form of a progress bar using the '#' character to represent completed portions, space to represent incomplete portions, and the actual percent done (rounded to integer) displayed in the middle:\n\n[#############     33%  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]\n\nWhen you initialize the class, you specify the minimum number (usually 0), the maximum number (your file size, for example), and the number of characters wide you would like the progress bar to be.  Note that width includes the brackets [] on the ends of the progress bar as well.\n\nYou'd probably want to use this in conjuction with the curses module, or something like that so you can over-write the same portion of the screen to make your updates 'animated'.