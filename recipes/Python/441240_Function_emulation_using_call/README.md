## Function emulation using __call__Originally published: 2005-10-14 03:07:25 
Last updated: 2005-11-21 02:15:46 
Author: Derrick Wallace 
 
A simple but useful class that emulates a function to gracefully permit latent assignment.  In other words, I can use the emulating class as a valid function in assignments with the ability to later associate a function to perfrom the actual operations.