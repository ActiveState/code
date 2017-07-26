## Remove the .pyc files from current directory tree and from svnOriginally published: 2009-02-03 23:38:43 
Last updated: 2009-02-03 23:38:43 
Author: Senthil Kumaran 
 
I had mistakenly checked in .pyc files into svn, So I took this approach of deleting all the .pyc files in the current working copy directory tree and then using svn remove to the remove from the repository. The following is the snippet I wrote then to for the purpose.