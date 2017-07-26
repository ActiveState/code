## Teach the hashbang header new tricks using a dual mode shell/python scriptOriginally published: 2011-08-21 07:27:04 
Last updated: 2011-08-21 07:27:05 
Author: Oren Tirosh 
 
This dual-mode script is both a Posix shell script and a python script. The shell part looks like a triple-quoted string to the Python interpreter. The shell does not reach anything after the exec statement.