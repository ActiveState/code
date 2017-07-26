###Recursive nlst() [was: FTP Directory Tree Retrieval]

Originally published: 2004-03-22 23:21:56
Last updated: 2006-07-27 14:27:13
Author: Rich Krauter

This recipe provides recursive nlst() behavior on top of a normal ftplib.FTP instance. The rnlst() method provided by the LocalFTP class returns a list of filenames under the path passed in as an argument.  (One use for this list might be mirroring an ftp site. However,  the python distribution contains a script called ftpmirror.py - use that instead.)\n\nBest suited for use on fast local connections, or for use on relatively small remote ftp directories.\n\nPlease see code comments for additional information.