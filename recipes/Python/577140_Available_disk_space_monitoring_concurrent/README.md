## Available disk space monitoring for concurrent writes

Originally published: 2010-03-23 12:32:45
Last updated: 2010-03-25 01:10:14
Author: Mateyuzo 

A DiskSpaceProctor is registered with a SyncManager to be shared by forked processes and threads. This object will check the available free space and add up filesz of concurrent writes. If there is not enough space for the requesting write, an exception is raised.