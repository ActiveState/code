## dal_6.py  
Originally published: 2006-04-26 10:29:40  
Last updated: 2006-09-30 00:29:59  
Author: Stephen Chappell  
  
DAL6 provides the cap of the Disk Abstraction
Layers and a way to create Context objects.
These Context objects provide relative paths
and keep track of the Currect Working
Directory. A method for renaming was
accidentally left out of the API. This
recipe also provides a full abstraction for
files involving full buffering and including
most of methods that should be expected.