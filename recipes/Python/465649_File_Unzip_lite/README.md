###File Unzip (lite)

Originally published: 2005-12-29 20:04:56
Last updated: 2005-12-30 05:13:58
Author: vishnubob 

This is a rewrite of <a href="http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/252508">Doug Tolton's</a> extract algorithm.  It's portable and small, ideal for paste-and-use.     NB: directory structure creation is slightly pendantic to ensure creation of implicit directories annotated by certain trixter zipfiles.  cStringIO guards against errors writing large files over 128MB in size.