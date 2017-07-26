## Terminating a subprocess on Windows

Originally published: 2004-11-24 12:52:28
Last updated: 2004-11-24 12:52:28
Author: Jimmy Retzlaff

The new subprocess module in Python 2.4 (also available for 2.2 and 2.3 at http://effbot.org/downloads/#subprocess) allows access to the handle of any newly created subprocess. You can use this handle to terminate subprocesses using either ctypes or the pywin32 extensions.