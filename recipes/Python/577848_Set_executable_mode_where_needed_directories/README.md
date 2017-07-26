## Set executable mode where needed: directories, ELF files and scripts

Originally published: 2011-08-18 17:41:07
Last updated: 2011-08-19 20:38:20
Author: Hector Rivas

If you make a mess (like I did) and you removed all the executable permissions of a directory (or you set executable permissions to everything) this can help.\n\nIt will walk through a tree of files setting or unsetting the executable mode of files or directories. \n\nNOTE: Will autodetect executables if they contain the word ELF at the beggining, so it won't work in platforms that does not use ELF (windows, AIX, etc).