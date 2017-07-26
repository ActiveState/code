## Executing modules inside packages with '-m' 
Originally published: 2004-10-09 08:46:03 
Last updated: 2004-10-10 19:03:49 
Author: Nick Coghlan 
 
Python 2.4 provides the '-m' option to run a module as a script. However, "python -m &lt;script&gt;" will report an error if the specified script is inside a package.\n\nPutting the following code in a module called "execmodule.py" and placing it in a directory on sys.path allows scripts inside packages to be executed using "python -m execmodule &lt;script&gt;".