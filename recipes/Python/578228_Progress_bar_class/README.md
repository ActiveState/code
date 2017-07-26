## Progress bar class

Originally published: 2012-07-28 21:26:15
Last updated: 2012-08-09 17:39:10
Author: Xavier L.

See [gist:3306295](https://gist.github.com/3306295) for future developments.\n\nHere is a little class that lets you present percent complete information in the form of a progress bar using the '=' character to represent completed portions, spaces to represent incomplete portions, '>' to represent the current portion and the actual percent done (rounded to integer) displayed at the end:\n\n[===========>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;] 60%\n\nWhen you initialize the class, you specify the minimum number (defaults to 0), the maximum number (defaults to 100), and the desired width of the progress bar. The brackets `[]` are included in the size of the progress bar, but you must allow for up to 4 characters extra to display the percentage.\n\nYou'd probably want to use this in conjuction with the curses module, or something like that so you can over-write the same portion of the screen to make your updates 'animated'.