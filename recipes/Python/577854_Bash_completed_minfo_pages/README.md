## Bash completed man and info pages generation  
Originally published: 2011-08-23 05:55:58  
Last updated: 2011-08-24 03:14:13  
Author: Josh D  
  
The script it self is very self explaining - the task is simple.
*NIX only unless with cygwin perhaps?

To start this open a terminal and strike the "Tab" key to get all possibilities (strike y, and strike the space key alot). Select all then Copy and save in "comms.txt"
Modify the file so ONLY the possiblities consume a line; no prompts or extra newlines.
  (first line must be a command, the last line must be a command)

Save the file ("~/Documents/bashing/comms.txt" is my path) then run this script in "~/Documents/bashing/".

This generates two (2) files: "bash_help_man.sh", "bash_help_info.sh".

Then it runs these files: "bash bash_help_man.sh", "bash bash_help_info.sh".

This produces 2 files for every command (every line) in "comms.txt".
All manpages are wrote in "mans/", all infopages are wrote in "infos/"

There is now alot of files to read and organize; lets separate these by size.
Directories are under1kb, under2kb, etc.

Once complete do as you wish the files less than 128 kb;
these files are COPIED into there new respective home, I repeat COPIED.

The files 128 kb and higher ARE NOT copied to anywhere!