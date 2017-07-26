## Run command in Win32 Registry 
Originally published: 2010-10-25 05:05:51 
Last updated: 2010-10-25 05:14:49 
Author: Phil Rist 
 
Each file type has several commands saved in the registry and associated with the\nfile type.  These commands appear in the context menu for files of that file type.\nIt seemed wasteful to replicate these commands with QEditor and Crimson Editor.\nDoCommand extracts the command from the registry, replaces macros and '%1' and '%*'\nstrings and executes the command similar to the Do.py program.