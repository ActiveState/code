## walk a local CVS directory tree 
Originally published: 2008-07-25 15:53:02 
Last updated: 2008-07-28 17:34:37 
Author: Alain Mellan 
 
There are times were I need to generate a manifest, or perform an export of my current CVS sandbox. cvs export works similarly to cvs co, i.e. extracts directly from a repository. I want to generate a clean export, without all the log files, etc, that tend to pollute my work area. I started using os.path.walk and remove what's not in CVS, but in the end the following code was much simpler (especially after taking a look at the source code for os.path.walk :-)