## A UNIX-like "which" command for Python

Originally published: 2015-03-20 19:23:44
Last updated: 2015-03-20 19:23:45
Author: Vasudev Ram

UNIX users are familiar with the which command. Given an argument called name, it checks the system PATH environment variable, to see whether that name exists (as a file) in any of the directories specified in the PATH. (The directories in the PATH are colon-separated on UNIX and semicolon-separated on Windows.)\n\nThis recipe shows how to write a minimal which command in Python.\nIt has been tested on Windows.\n