## Determining Current Function Name

Originally published: 2001-07-17 03:24:20
Last updated: 2001-07-17 03:24:20
Author: Alex Martelli

You want to determine the name of the currently running function, e.g. to create error messages that don't need to be changed when copied to other functions.  Function _getframe of module sys does this and much more.