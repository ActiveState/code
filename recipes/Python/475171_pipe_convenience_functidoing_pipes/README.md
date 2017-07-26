## pipe convenience function for doing pipes as in bash 
Originally published: 2006-03-24 00:38:28 
Last updated: 2006-03-24 00:38:28 
Author: George Benko 
 
Allows arbitrary number of commands to be strung together with each one feeding into the next ones input. Syntax is simple: x=pipe("cmd1", "cmd2", "cmd3").read() is equivalent to bash command x=`cmd1 | cmd2 | cmd3`.\n\nWorks under python 2.4.2