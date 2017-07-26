###Colour Bar And Greyscale Generator For Standard Text Mode Python.

Originally published: 2013-01-18 21:08:20
Last updated: 2013-01-18 21:08:21
Author: Barry Walker

This is just a simple colour bar and combined greyscale generator for standard text mode Python...\n\nIt relies on the _magic_ of the ANSI Escape sequences to work and does mess with the terminal colours but restores the colours back to the defaults...\n\nSee the code for the machines tested on. It might need the colours adjusting for some terminals but I am sure that is not beyond the average coder...\n\nWritten so that anyone can see how it works.\n\nTo hide the cursor the command "tput" is assumed to be available, if not, try "setterm -cursor off" and "setterm -cursor on" instead...\n\nEnjoy...\n\nBazza, G0LCU...\n