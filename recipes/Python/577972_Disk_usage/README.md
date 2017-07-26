## Disk usage  
Originally published: 2011-12-02 11:56:17  
Last updated: 2012-10-06 15:33:40  
Author: Giampaolo Rodolà  
  
Provides disk usage statistics (total, used and free disk space) about a given path.

This recipe was initially developed for psutil:

 * http://code.google.com/p/psutil/issues/detail?id=172

...and then included into shutil module starting from Python 3.3:

 * http://mail.python.org/pipermail/python-ideas/2011-June/010480.html
 * http://bugs.python.org/issue12442
 * http://docs.python.org/dev/library/shutil.html#shutil.disk_usage

The recipe you see here is a modified version of the latter one in that the Windows implementation uses ctypes instead of a C extension module. As such it can be used with python >= 2.5.