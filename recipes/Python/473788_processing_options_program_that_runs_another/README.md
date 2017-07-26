###processing options for a program that runs another program that has its own options

Originally published: 2006-01-26 09:06:22
Last updated: 2006-01-26 09:06:22
Author: Rocky Bernstein

I have a program, say a debugger, that runs another program which has options of its own. I want people to be able to give options to either program and don't want them to get confused. For example, perhaps both have "--help" options.\n\nSo to be a little more concrete, let's say I'd like to run say program (pdb) and have it pass "--help" to a program I want it to run (specified as a command argument) called "debugged-script". I'd like to issue the command like this:\n\npdb --trace debugged-script --help\n\nand have "--help" go to "debugged-script" and not "pdb".