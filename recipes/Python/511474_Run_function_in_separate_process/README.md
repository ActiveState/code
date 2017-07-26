## Run function in separate process 
Originally published: 2007-04-15 17:45:08 
Last updated: 2008-05-04 12:48:23 
Author: Muhammad Alkarouri 
 
This is a simple function that runs another function in a different process by forking a new process which runs the function and waiting for the result in the parent. This can be useful for releasing resources used by the function such as memory.